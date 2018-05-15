# -*- coding: utf-8 -*-
"""
该模块定义数据图层概念。并且定义具体数据类型图层

 - writer:linux_23; create: ; version:1; 创建
 - linux_23: 2007.5.29; 在layer中添加labelProps成员
 - linux_23: 2008.4.13; 大修改，去掉繁多的Open方法，分离栅格矢量的打开
"""
import DataSet
import gdal,ogr,os
from gssconst import *
from Numeric import *
from math import *
from geosings.core.system import *
from geosings.core.system.GLog import *
import time
from Exception import *
from GeoRect import Rect,GeoRect
from Symbol import CreateSymbol
from GeomWkt import *

def CheckPGOgrConnStr(connstr):
    """PG的连接字符串需要改动,去掉多余的"
    """
    if connstr.startswith('PG:"'):
        connstr = 'PG:'+connstr[4:len(connstr)-1]
    return connstr

def GetLayer(source,name="",update=0):
    """该函数代替gdal的Open函数，作为打开数据集的入口
    @type source: str
    @param source: 要打开的图层的路径或者连接字符串
    @rtype: L{geosings.core.Layer}
    @return: 返回打开的图层
    """
    source = CheckPGOgrConnStr(source) #保持PG的连接字符串正确性，其余不变
	
    dataSource = ogr.Open(source,update)
    if name!="":
        layer = VectorLayer(dataSource.GetLayer(name),dataSource,source)
        return layer
    layercount = dataSource.GetLayerCount()
    if layercount>1:
        layer = []
        for i in range(layercount):
            layer.append(VectorLayer(dataSource.GetLayer(i),dataSource,source,
                GetFileNameNoExt(source)))
        return layer
    else:
        layer = VectorLayer(dataSource.GetLayer(),dataSource,source)
        return layer

def WalkFeatures(features,fun):
    """在一个Feature列表中对所有feature运行某个函数,并检出一个新的列表
    @type features: GDAL Feature
    @param features: 要运行操作的要素列表
    @type fun: function
    @param fun: 要运行的函数
    @rtype: list
    @return: 返回一个运行函数后形成的新的列表
    """
    return [fun(f) for f in features]

def GetFeatureDataFormat():
    """获取可以使用的矢量数据格式
    """
    return [ogr.GetDriver(i).GetName() for i in range(ogr.GetDriverCount())]

def GetRasterDataFormat():
    """获取可以使用的栅格数据格式
    """
    return [i.LongName for i in gdal.GetDriverList()]

class Layer:
    """定义图层基类，不建议进行实例化
    """
    def __init__(self,dataset,path):
        """初始化
        @type dataset: L{geosings.core.DataSet}
        @param dataset: 在Layer里使用的数据集，是实际数据存在之处
        @type path: str
        @param path: dataset所在的路径
        """
        self.name = ""
        self.dataset = dataset
        self.type = DataSetType.Unknown
        self.visual = 1
        self.path = path
        self.labelProps = None
        self.render = None

    def __getattr__(self, name):
        """让用户可以透过dataset层调用gdal或ogr的函数或方法
        """
        return getattr(self.dataset, name)

    
    def GetTypeName(self):
        """获取数据图层类型的名字
        @rtype: str
        @return: 返回数据图层类型的名字
        """
        return dstStrMap[self.type]

    def DataSet(self):
        """获取作为数据操作基础的数据集
        @rtype: L{geosings.core.DataSet}
        @return: 返回数据集
        """
        return self.dataset

    def CacDrawArgs(self,dcrect,dcgeoext):
        """计算绘制参数
        @type dcrect: L{geosings.core.GeoRect}
        @param dcrect: 图像范围
        @type dcgeoext: L{geosings.core.GeoRect}
        @param dcgeoext: 地图的地理范围
        @rtype: list
        @return: 返回一个列表，下面是返回列表的每个元素解释
                 - x:返回图像的X
                 - y:返回图像的Y
                 - bw:返回图像取值窗口的宽(bufw)
                 - bh:返回图像取值窗口的高(bufh)
                 - mx:在地图矩形中的图像的X
                 - my:在地图矩形中的图像的Y
        """
        dcdleft,dcdtop = self.GeoPToDataP(
                dcgeoext.GetLeft(),
                dcgeoext.GetTop())
        dcdright,dcdbottom = self.GeoPToDataP(
                dcgeoext.GetRight(),
                dcgeoext.GetBottom())
        dcdw = fabs(dcdright-dcdleft)# data width in dc rect
        dcdh = fabs(dcdbottom-dcdtop)# data height in dc rect
        if dcdleft<0:# left out of data
            datamx = -dcdleft # real data left move
            dcdleft = 0 # real data read point x
            x = 0 # data left move 
        else:
            datamx = 0
            x = dcdleft
        if dcdtop<0:# top out of data
            datamy = -dcdtop
            dcdtop = 0
            y = 0 # data top move
        else:
            datamy = 0
            y = dcdtop
        if dcdright>self.width:# right out of data
            w = self.width-x
        else: w = dcdright-x
        if dcdbottom>self.height:# height out of data
            h = self.height-y
        else: h = dcdbottom-y

        dcw = dcrect.GetWidth() # dc 's width
        dch = dcrect.GetHeight() # dc 's height
        dw = (dcw*w*1.0)/dcdw
        dh = (dch*h*1.0)/dcdh
        mx = (datamx*dw*1.0)/w
        my = (datamy*dh*1.0)/h
        #debug( 'cac result:',x,y,w,h,dw,dh,mx,my)

        return  x,y,w,h, \
                dw,dh,mx,my

    def GeoPToDataP(self,x,y):
        """根据地理点获取对应的数据点
        @type x:number
        @type y: number
        @param x,y: 地理点的X,Y
        @rtype: number
        @return: 对应的图像X,Y
        """
        gw = self.DataGeoExt.GetWidth() 
        gx = self.DataGeoExt.GetLeft()
        gh = self.DataGeoExt.GetHeight()
        gy = self.DataGeoExt.GetTop()
        dw = self.DataExt.GetWidth()
        dh = self.DataExt.GetHeight()
        xdw = dw*(gx-x)/(gw*1.0)
        xdh = dh*(gy-y)/(gh*1.0)
        dx = self.DataExt.GetLeft()
        dy = self.DataExt.GetTop()
        return dx-xdw,dy+xdh

class RasterLayer(Layer):
    """栅格的图层类
    """
    def __init__(self,dataset,path):
        """初始化
        """
        Layer.__init__(self,dataset,path)
        self.type = DataSetType.Raster
        if self.DataSet() is None:
            #mainDocument.ErrNo = ErrorNum.FileNoFoundErr
            #raise FileNotFoundErr#,'File'+path+' is not exist!' 
            raise GssException(ErrorNum.FileNoFoundErr)
        else:
            debug('gtif Dataset has opened!')
            self.name = GetFileNameNoExt(self.path)
            self.width = self.DataSet().RasterXSize
            self.height = self.DataSet().RasterYSize
            self.bandCount = self.DataSet().RasterCount
            self.__initGeoRef()

    def __initGeoRef(self):
        """初始化地理范围和空间参考
        """
        adfGeoTrans = self.DataSet().GetGeoTransform()
        if adfGeoTrans is not None:
            x1 = adfGeoTrans[0]*1.0
            y1 = adfGeoTrans[3]*1.0
            x2 = x1+adfGeoTrans[1]*self.width+ \
                    adfGeoTrans[2]*self.height
            y2 = y1+adfGeoTrans[4]*self.width+ \
                    adfGeoTrans[5]*self.height
            #xo = x1 ; yo = y2
            #geow = fabs(x2-x1)
            #geoh = fabs(y2-y1)
        else:
            debug('have no geo extend')
            #xo = 0 ; yo = 0 
            x1 = 0 ; y1 = 0
            x2 = self.width; y2 = self.height
            #geow = self.width 
            #geoh = self.height
        grect = GeoRect(x1,y1,x2,y2)
        debug( 'geoext:%s',grect)
        self.DataGeoExt = grect
        self.DataExt = Rect(0,0,self.width,self.height)
        self.sr = self.DataSet().GetProjectionRef()


class VectorLayer(Layer):
    """矢量的图层类
    """
    def __init__(self,dataset,datasource,path,parentname=""):
        """初始化
        @type dataset: L{geosings.core.DataSet}
        @param dataset: 在Layer里使用的数据集，是实际数据存在之处
        @type path: str
        @param path: dataset所在的路径
        @type parentname: str
        @param parentname: 父数据集名称
        """
        Layer.__init__(self,dataset,path)
        self.type = DataSetType.Vector
        self.dataSource = datasource
        if self.DataSet() is None:# failuse
            #mainDocument.ErrNo = ErrorNum.FileNoFoundErr
            #raise FileNotFoundErr
            raise GssException(ErrorNum.FileNoFoundErr)
        else: # init the data
            debug( 'shape Dataset has opened!')
            if parentname is None:
                self.name = self.DataSet().GetName()
            elif len(parentname)==0:
                self.name = self.DataSet().GetName()
            else:
                self.name = "-".join([self.DataSet().GetName(),parentname])
            #self.layerCount = self.DataSet().GetLayerCount()
            #self.sublayers = []
            #for i in range(self.layerCount):
            #    self.sublayers.append(self.DataSet().GetLayer(i))
            self.__initGeoRef()# init the geo reference info
            geomtype = self.DataSet().GetLayerDefn().GetGeomType()
            self.symbol = CreateSymbol(geomtype)
            
    def __initGeoRef(self):
        """初始化地理范围和空间参考
        """
        #self.__geoexts = []
        self.DataGeoExt = None
        #for i in range(self.layerCount):
        #ext = self.sublayers[i].GetExtent()
        ext = self.DataSet().GetExtent()
        if ext[0]==ext[1] or ext[2]==ext[3]:#如果是一个点的情况
            x1=ext[0]-0.5
            x2=ext[1]+0.5
            y1=ext[2]-0.5
            y2=ext[3]+0.5
        else:
            x1,x2,y1,y2 = ext[0],ext[1],ext[2],ext[3]
        self.geoext = GeoRect(x1,y1,x2,y2)
        #self.__geoexts.append(self.geoext)
        #self.__geoexts = self.geoext
        #if i == 0:
        self.DataGeoExt = self.geoext # init self.datageoext
        #else :
        #    if self.geoext.GetLeft()<self.DataGeoExt.GetLeft():
        #        self.DataGeoExt.SetLeft(self.geoext.GetLeft())
        #    if self.geoext.GetRight()>self.DataGeoExt.GetRight():
        #        self.DataGeoExt.SetRight(self.geoext.GetRight())
        #    if self.geoext.GetTop()>self.DataGeoExt.GetTop():
        #        self.DataGeoExt.SetTop(self.geoext.GetTop())
        #    if self.geoext.GetBottom()<self.DataGeoExt.GetBottom():
        #        self.DataGeoExt.SetBottom(self.geoext.GetBottom)
        
        self.height = self.DataGeoExt.GetHeight()
        self.width = self.DataGeoExt.GetWidth()
        self.DataExt = GeoRect(0,0,self.width,-self.height)
        #self.DataExt = Rect(0,0,1,1)
        self.sr = self.DataSet().GetSpatialRef()
        if self.sr is None:
            self.sr = ""

        debug('geoext:%s',self.DataGeoExt)

    def SelectFeatures(self,geometry):
        """选择图层中和给定几何形状相交的要素形成列表返回
        @type geometry: Geometry
        @param geometry: 要进行判断的几何形状
        @rtype: list
        @return: 返回图层中和给定的几何形状相交的要素列表
        """
        dataset = self.DataSet()
        #dataset.ResetReading()
        dataset.SetSpatialFilter(geometry)
        fs = []
        f = dataset.GetNextFeature()
        while f is not None:
            g = f.GetGeometryRef()
            if geometry.Intersect(g): fs.append(f)
            #fs.append(f)
            f = dataset.GetNextFeature()
        debug("selection count:%d",len(fs))
        return fs
    
    def SelectFeaturesByPoint(self,point,dcrect,geoext):
        """选择图层中和给定几何形状相交的要素形成列表返回
        @type point: list
        @param point: 要进行选取的点坐标
        @rtype: list
        @return: 返回图层中和给定的点要素所处在的要素列表
        """
        px,py = ScreenPToGeoP(point[0],point[1],dcrect,geoext) 
        p1x,p1y = ScreenPToGeoP(point[0]-2,point[1]-2,dcrect,geoext) 
        p2x,p2y = ScreenPToGeoP(point[0]+2,point[1]+2,dcrect,geoext)
        wkt = CreatePolygonWkt([[p1x,p1y],
            [p1x,p2y],[p2x,p2y],[p2x,p1y],[p1x,p1y]])
        geometry = ogr.CreateGeometryFromWkt(wkt)
        dataset = self.DataSet()
        geomtype = dataset.GetLayerDefn().GetGeomType()
        if geomtype == ogr.wkbPoint:
            return self.SelectFeatures(geometry)
        #dataset.ResetReading()
        dataset.SetSpatialFilter(geometry)
        fs = []
        from PILImageDC import PILByteImageDC
        f = dataset.GetNextFeature()
        while f is not None:
            g = f.GetGeometryRef()
            #计算绘制参数
            extent = g.GetEnvelope()
            tmpgeow = geoext.GetWidth()
            tmpgeoh = geoext.GetHeight()
            geowidth = math.fabs(extent[1]-extent[0])
            geoheight = math.fabs(extent[3]-extent[2])
            dcw = dcrect.GetWidth()
            dch = dcrect.GetHeight()
            width = geowidth/tmpgeow*dcw
            height = geoheight/tmpgeoh*dch
            if width>dcw or height>dch:#图像太大(超过屏幕范围)不可能全绘
                minx = geoext.GetLeft()
                maxy = geoext.GetTop()
                scale = dcw/tmpgeow
                width = dcw
                height = dch
            else:#小的就全绘吧！
                minx = min(extent[0],extent[1])
                maxy = max(extent[3],extent[2])
                scale = width/geowidth
            atx = int((px-minx)*dcw/tmpgeow)
            aty = int((maxy-py)*dch/tmpgeoh)
            width = int(width); height = int(height)
            if width == 0 : fs.append(f);f=dataset.GetNextFeature();continue
            if height == 0 : fs.append(f);f=dataset.GetNextFeature();continue
            #debug( 'xy',atx,aty,width,height)
            if atx<0 or aty<0 or atx>width or aty>height:#不在矩形内就不用判断了
                debug( 'ingore:%s',f.GetFID())
                f= dataset.GetNextFeature()
                continue
            
            imgdc = PILByteImageDC()
            imgdc.DrawAGeoRef(g,width,height,minx,maxy,scale)
            #imgdc.im.putpixel((atx,aty),1)
            #imgdc.im.save('f:/gisdata/'+str(f.GetFID())+'.png','png')
            if geomtype == ogr.wkbPolygon:
                pixarr = [imgdc.im.getpixel((atx,aty))]
            else:
                box = (atx-2,aty-2,atx+2,aty+2)
                pixarr = list(imgdc.im.crop(box).getdata())
            
            if 255 in pixarr:
                fs.append(f)
            f = dataset.GetNextFeature()
        debug( "selection count:%d",len(fs))
        return fs

    def SetAttributeFilter(self,strFilter,codec=None):
        """设置属性过滤器
        @type strFilter: str
        @param strFilter: 属性过滤条件（where语句）
        @type codec: str
        @param codec: 属性条件的字符编码(用在数据和locale编码不一样时)
        """
        from geosings.core.system.EncodeTran import astr2sth
        if codec is not None and codec!="":
            strFilter = astr2sth(strFilter,codec)
        self.DataSet().SetAttributeFilter(strFilter)

def OpenV(path,update=0,forceType=None):
    """打开一个矢量的Layer，作为静态的函数
    @type path: str
    @param path: Layer的路径
    @type forceType: str
    @param forceType: 需要指定的驱动名(如果需要用和默认的驱动不同驱动的时候指定)
    @rtype: L{geosings.core.Layer}
    @return: 返回打开的图层
    """
    debug("now want to open path:%s",path)
    if forceType is None or forceType == "ogr":
        try:
            return GetLayer(path,update=update)
        except:
            raise
    else:
        raise UnOpenDataSetExcepion
def OpenVSource(path,update=0,forceType=None):
    """打开一个矢量的DataSource，作为静态的函数
    @type path: str
    @param path: Layer的路径
    @type forceType: str
    @param forceType: 需要指定的驱动名(如果需要用和默认的驱动不同驱动的时候指定)
    @rtype: ogr.DataSource
    @return: 返回打开的图层
    """
    debug("now want to open path:%s",path)
    if forceType is None or forceType == "ogr":
        try:
            return ogr.Open(path, update)
        except:
            raise
    else:
        raise UnOpenDataSetExcepion

def CreateVLayer(datasource, name, srs, type, fieldDefns):
    """创建一个矢量图层
    @type datasource: ogr.DataSource
    @param datasource: 要创造矢量图层的数据源
    @type name: str
    @param name: 要创建的图层名称
    @type srs: osr.SpatialReference
    @param srs: 图层参考坐标系
    @type type: int
    @param type: 要创建的图层类型（点，线，面）
    @type fieldDefns: array
    @param fieldDefns: 字段描述的定义数组
    @rtype: layer
    @return: 返回创建的图层（要保存需要Close）
    """
    layer = datasource.CreateLayer(name, srs, type)
    for fieldDefn in fieldDefns:
        layer.CreateField(fieldDefn)
    return layer

def OpenR(path,forceType=None):
    """打开一个栅格的Layer，作为静态的函数
    @type path: str
    @param path: Layer的路径
    @type forceType: str
    @param forceType: 需要指定的驱动名(如果需要用和默认的驱动不同驱动的时候指定)
    @rtype: L{geosings.core.Layer}
    @return: 返回打开的图层
    """
    if forceType is None:
        dataset = gdal.Open(path)
        layer = RasterLayer(dataset,path)
        return layer
    
#def Open(path):
#    """打开一个Layer(用默认的方法，不分栅格矢量)，作为静态的函数
#    @type path: str
#    @param path: Layer的路径
#    @rtype: L{geosings.core.Layer}
#    @return: 返回打开的图层
#    """
#    return Layer.Open(path)

class LayerUtil:
    """Layer的辅助类
    """
    def __init__(self, layer):
        self.layer = layer
        self.dataSource = self.layer.dataSource
        #self.dataset = self.layer.DataSet()
        self.dataset = self.layer
        self.driver = self.dataSource.GetDriver()

    def CopyDataset(self,oDataset):
        """拷贝数据集
        """
        layerDef = self.dataset.GetLayerDefn()
        newlayerDef = oDataset.GetLayerDefn()
        #创建Field表头，只要有表头，CreateFeature就会根据表头，自动拷贝Field的值
        for i in range(layerDef.GetFieldCount()):
            defn = layerDef.GetFieldDefn(i)
            oDataset.CreateField(defn)
        feature = self.dataset.GetNextFeature()
        while feature is not None:
            oDataset.CreateFeature(feature)
            feature = self.dataset.GetNextFeature()

    def ConvertXYs(self, conv_fun, oDataset):
        """转换XY的坐标
        """
        layerDef = self.dataset.GetLayerDefn()
        newlayerDef = oDataset.GetLayerDefn()
        #创建Field表头，只要有表头，CreateFeature就会根据表头，自动拷贝Field的值
        for i in range(layerDef.GetFieldCount()):
            defn = layerDef.GetFieldDefn(i)
            oDataset.CreateField(defn)

        feature = self.dataset.GetNextFeature()
        while feature is not None:
            nf = feature.Clone()
            geom = nf.GetGeometryRef()
            self.__walkGeom(geom,conv_fun)
            oDataset.CreateFeature(nf)
            feature = self.dataset.GetNextFeature()

    def __walkGeom(self,geom,conv_fun):
        """递归遍历几何形状"""
        if geom is None:
            return 
        subcount = geom.GetGeometryCount()
        for i in range(subcount):
            subgeom = geom.GetGeometryRef(i)
            self.__walkGeom(subgeom,conv_fun)
        pointcount = geom.GetPointCount()
        for p in range(pointcount):
            newx,newy = conv_fun(geom.GetX(p),geom.GetY(p))
            geom.SetPoint_2D(p,newx,newy)
