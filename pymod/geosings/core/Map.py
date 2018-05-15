# -*- coding: utf-8 -*-
"""
该模块管理一系列的图层对象

 - writer:linux_23; create: ; version:1; 创建
 - linux23; 2007.9.12; 把LayerManager改名为Map
 - linux23; 2008.4.13; 在AddLayer后添加计算总地理范围的函数
"""

import Layer
from GeoRect import GeoRect
from Exception import *
from geosings.core.gssconst import *
from geosings.core.system.GLog import *

class Map:
    """该类管理一系列的图层对象
    """
    def __init__(self,layers=None):
        """初始化
        @type layers: list
        @param layers: 需要初始化的图层
        """
        if layers is None: self.layers=[]
        else: self.layers=layers

        #整个图层的地理范围
        self.allGeoExt = GeoRect(0,0,1,1)
        #各个图层的地理范围的列表
        self.DataGeoExt = []#None
        #各个图层的数据范围的列表
        self.DataExt = []#None

        #选择了的图层列表
        if len(self.layers)==0:
            self.__selections = []
        else:
            self.__selections = [0]
        
        self.whereLayer = ""
        self.whereFlite = ""
        self.codec = None
    
    def SetWhere(self, layer, where, codec=None):
        self.whereLayer = layer
        self.whereFlite = where
        self.codec = codec

    def SelectLayers(self,items):
        """选择某些图层
        @type items: list
        @param items: 要选择作为操作图层的图层索引列表
        """
        self.__selections = items
        #print "select layer:",items

    def GetSelectedLayersItems(self):
        """获取选择的图层索引列表
        @rtype: list
        @return: 返回被选择的图层索引列表
        """
        return self.__selections

    def GetSelectedLayers(self):
        """获取选择的图层索引列表
        @rtype: list
        @return: 返回被选择的图层名列表
        """
        return [self.GetLayer(i) for i in self.__selections]

    def GetLayers(self):
        """获取所管理的图层列表
        @rtype: list
        @return: 返回所管理的图层列表
        """
        return self.layers

    def AddLayer(self,layer):
        """添加一个单一的图层到文档中
        @type layer: L{geosings.core.Layer}
        @param layer: 要添加到文档中的图层
        """
        self.layers.append(layer)
        self.DataGeoExt.append(layer.DataGeoExt)
        self.DataExt.append(layer.DataExt)
        self.__selections = [i+1 for i in self.__selections]
        self.CacAllDataGeoExt()
        self.CacAllDataExt()

    def FindLayerName(self,layername):
        """查找一个指定名字的图层
        @type layername: str
        @param layername: 指定图层名
        @rtype: int
        @return: 查找到的图层在文档中的索引,从0开始,如果没有找到,返回-1
        """
        findn = 0
        for l in self.layers:
            #print l.name,layername
            if l.name == layername:
                return findn
            findn += 1
        self.ErrNo = ErrorNum.LayerNoFoundErr
        return -1
    def RemoveLayer(self,layer=None):
        """移除一个图层
        @type layer: str,Layer
        @param layer: 要移除的图层（放空则移除已经选择的图层）
        """
        if layer is None: # 需要移除所有已经选择的图层
            rm_names = [] #要移除的图层名称集合
            for i in self.__selections:
                findn = self.GetLayerAt(i)
                rm_names.append(self.layers[findn].name)
            #递归移除已经选择的图层
            for name in rm_names:
                self.RemoveLayer(name)
            self.__selections = [] #已选集设空
            return

        #移除制定名称的图层
        findn = 0
        laylen = len(self.layers)
        for l in self.layers:
            if type(layer)==str or type(layer)==unicode:
                lobj = l.name
            else:
                lobj = l
            if lobj == layer:
                self.layers.remove(l)
                del l
                if findn in self.__selections:
                    self.__selections.remove(findn)#如果有选择，移除选择
                self.DataGeoExt.remove(self.DataGeoExt[findn])
                self.DataExt.remove(self.DataExt[findn])
                self.CacAllDataGeoExt()
                self.CacAllDataExt()
                findn+=1
                break
            else:
                findn+=1
                    
        if laylen== len(self.layers):
            raise LayerNoFoundErr

    def MoveFromTo(self,fromwhere,towhere):
        """把一个图层移动到指定索引中
        @type fromwhere: int
        @param fromwhere: 要移动图层的索引
        @type towhere: int
        @param towhere: 要移动到什么位置
        """
        if len(self.layers)<2:
            return 
        fw,tw = fromwhere,towhere
        fromwhere = len(self.layers)-1-fromwhere
        towhere = len(self.layers)-1-towhere
        #print "doc move to",fromwhere,towhere
        layer = self.layers.pop(fromwhere)
        dge = self.DataGeoExt.pop(fromwhere)
        de = self.DataExt.pop(fromwhere)
        self.layers.insert(towhere,layer)
        self.DataGeoExt.insert(towhere,dge)
        self.DataExt.insert(towhere,de)

        tmp = None
        if fw in self.__selections:
            tmp = fw #如果移动的是已选的，在pop和push过程中会丢失
        sels = [self.__andors(i, fw) for i in self.__selections]
        self.__selections = [self.__andorp(i, tw) for i in sels]
        if tmp is not None:
            self.__selections.append(tmp) #避免已选的项在移动过程中丢失

    def __andors(self,i , flag):
        if i >flag: return i-1#大于fromwhere的向下移动
        else: return i
    def __andorp(self,i, flag):
        if i>=flag: return i+1#大等于towhere的向上移动
        else: return i

    def TopLayer(self,layern):
        """使一个图层处于最上层
        @type layern: int或者str
        @param layern: 要移动到最上层的图层的名字或者索引
        """
        findn = self.GetLayerAt(layern)
        if findn != -1:
            layeri = self.layers[findn]
            self.layers.remove(layeri)
            self.layers.append(layeri)
            dgei = self.DataGeoExt[findn]
            self.DataGeoExt.remove(dgei)
            self.DataGeoExt.append(dgei)
            dei = self.DataExt[findn]
            self.DataExt.remove(dei)
            self.DataExt.append(dei)
            if findn in self.__selections:#如果涉及选择，重新排列选择
                self.__selections.append(self.__selections.pop(findn))
        else:
            raise LayerNoFoundErr

    def GetLayerAt(self,layern):
        """查找图层所处的位置
        @type layern: int或者str或者unicode
        @param layern: 要查找的图层的名称或者索引
        @rtype: int
        @return: 图层所处的位置的索引,从0开始,-1为没有找到
        """
        if type(layern)==type("") or type(layern)==type(u""):
            findn = self.FindLayerName(layern)
        elif type(layern) == int:
            findn = len(self.layers)-1-layern
        else:
            findn = -1
        debug( 'find layer: %s', findn)
        return findn

    def VisibleLayer(self,layern,v):
        """让一个图层可见(或者不可见)
        @type layern: int或者str
        @param layern: 要可见(或不可见)的图层的名称或者索引
        @type v: bool
        @param v: 使其可见或者不可见
        """
        findn = self.GetLayerAt(layern)
        if findn != -1:
            self.layers[findn].visual = v
        else:
            raise LayerNoFoundErr

    def GetLayer(self,layern):
        """获取指定图层
        @type layern: str或int
        @param layern: 要获取的图层的名称或者索引
        @rtype: L{geosings.core.Layer.Layer}
        @return: 指定图层
        """
        findn = self.GetLayerAt(layern)
        if findn != -1:
            debug("%s %s",findn,self.layers[findn])
            return self.layers[findn]
        else:
            error("can't find layer %s", layern)
            return None

    def GetFeaturesByGeometry(self,geometry):
        """由一个几何形状获取图层中的要素集合
        @type geometry: OGC Geometry
        @param geometry: 给定的几何形状
        @rtype: list
        @return: 返回由几何形状挑出的要素组成的列表
        """
        if len(self.layers)==0:
            return []
        if len(self.__selections)==0:
            return []
        layer = self.layers[self.GetLayerAt(max(self.__selections))]
        if layer.type == DataSetType.Vector:
            return layer.SelectFeatures(geometry)
        else:
            return []
    def GetFeaturesByPoint(self,point,dcrect,geoext):
        """由一个几何形状获取图层中的要素集合
        @type geometry: OGC Geometry
        @param geometry: 给定的几何形状
        @rtype: list
        @return: 返回由几何形状挑出的要素组成的列表
        """
        if len(self.layers)==0:
            return []
        if len(self.__selections)==0:
            return []
        layer = self.layers[self.GetLayerAt(max(self.__selections))]
        if layer.type == DataSetType.Vector:
            return layer.SelectFeaturesByPoint(point,dcrect,geoext)
        else:
            return []
    def GetLayerCount(self):
        """获取已经读取的图层总数
        @rtype: int
        @return: 返回已经读取的图层总数
        """
        return len(self.layers)

    def CacAllDataGeoExt(self):
        """计算所有的数据说覆盖的地理空间范围
        @rtype: list
        @return: 返回由空间范围长宽组成的列表
        """
        if(len(self.DataGeoExt)>0):
            left = self.DataGeoExt[0].GetLeft()
            right = self.DataGeoExt[0].GetRight()
            top = self.DataGeoExt[0].GetTop()
            bottom = self.DataGeoExt[0].GetBottom()
            for de in self.DataGeoExt:
                if de.GetLeft()<left:
                    left = de.GetLeft()
                if de.GetRight()>right:
                    right = de.GetRight()
                if de.GetTop()>top:
                    top = de.GetTop()
                if de.GetBottom()<bottom:
                    bottom = de.GetBottom()
            self.allGeoExt.ReSet(left,top,right,bottom)
            return self.allGeoExt.GetWidth(),self.allGeoExt.GetHeight()

    def CacAllDataExt(self):
        """计算所有的数据范围（数据实际范围，比如栅格图像的宽高）
        @rtype: list
        @return: 返回数据的宽高组成的列表
        """
        if(len(self.DataExt)>0):
            dataw = self.DataExt[0].GetWidth()
            datah = self.DataExt[0].GetHeight()
            geow = self.DataGeoExt[0].GetWidth()
            geoh = self.DataGeoExt[0].GetHeight()
            if geow==0 or geoh ==0 or dataw==0 or datah==0:
                return 0,0
            vdw = self.allGeoExt.GetWidth()/geow*dataw
            vdh = self.allGeoExt.GetHeight()/geoh*datah
            return vdw,vdh

    def initGeoExt(self,dcw,dch):
        """初始化地理范围,放大到全图
        @type dcw: int
        @param dcw: 绘制屏幕的宽
        @type dch: int
        @param dch: 绘制屏幕的高
        """
        datageow,datageoh=self.CacAllDataGeoExt()
        dataow,dataoh = self.CacAllDataExt()
        if dataow*1.0/dataoh < dcw*1.0/dch: # an height
            dataw = dch*dataow/dataoh # the dc w covered by data(screen unit)
            datah = dch               # the dc h covered by data(screen unit)
        else:
            datah = dcw*dataoh/dataow # the dc w covered by data(screen unit)
            dataw = dcw               # the dc h covered by data(screen unit)
        allgeoW = datageow*dcw/dataw  # the geo ext cover the screen
        allgeoH = datageoh*dch/datah  # the geo ext cover the screen
        midpx,midpy = self.allGeoExt.GetMiddlePoint()
        allgeoy = midpy-allgeoH/2
        allgeox = midpx-allgeoW/2
        allgeox2 = allgeox+allgeoW
        allgeoy2 = allgeoy+allgeoH
        self.allGeoExt.ReSet(allgeox,allgeoy,allgeox2,allgeoy2)
        #self.geoext = self.allGeoExt


