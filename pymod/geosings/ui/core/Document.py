# -*- coding: utf-8 -*-
"""
该模块定义文档对象

 - writer:linux_23; create: ; version:1; 创建
 - linux_23; 2007.6.16; 修改导出代码使Document包位置正确
"""

import math,os
from geosings.core.system import *
from geosings.core.GeoRect import GeoRect
from geosings.core.system.FillLine import fillline
from geosings.core.gssconst import *
from geosings.core.Exception import *
from geosings.core.Map import Map as GSSMap


class Document:
    """文档类
    """
    def __init__(self):
        """初始化
        """
        self.ReInit()


    def ReInit(self):
        """将文档重新初始化
        """
        self.commond = []
        #下面是现在要绘制的范围
        self.geoext = None

        self.map = GSSMap()

        self.zoomall = 1
        self.ErrNo = 0
        # set the default value
        self.panStep = 20
        fillline.SetLayers(self.map.GetLayers())


    def initGeoExt(self,dcw,dch):
        """初始化地理范围,放大到全图
        @type dcw: int
        @param dcw: 绘制屏幕的宽
        @type dch: int
        @param dch: 绘制屏幕的高
        """
        datageow,datageoh=self.map.CacAllDataGeoExt()
        dataow,dataoh = self.map.CacAllDataExt()
        if dataow*1.0/dataoh < dcw*1.0/dch: # an height
            dataw = dch*dataow/dataoh # the dc w covered by data(screen unit)
            datah = dch               # the dc h covered by data(screen unit)
        else:
            datah = dcw*dataoh/dataow # the dc w covered by data(screen unit)
            dataw = dcw               # the dc h covered by data(screen unit)
        allgeoW = datageow*dcw/dataw  # the geo ext cover the screen
        allgeoH = datageoh*dch/datah  # the geo ext cover the screen
        midpx,midpy = self.map.allGeoExt.GetMiddlePoint()
        allgeoy = midpy-allgeoH/2
        allgeox = midpx-allgeoW/2
        allgeox2 = allgeox+allgeoW
        allgeoy2 = allgeoy+allgeoH
        self.map.allGeoExt.ReSet(allgeox,allgeoy,allgeox2,allgeoy2)
        #self.geoext = self.allGeoExt

    def ReInitGeoExt(self):
        """重新放大到全图
        """
        self.zoomall=1

    def OpenDocument(self,path,force=False):
        """打开一个外部设置的文档设置
        @type path: str
        @param path: 外部文档的位置
        @type force: bool
        @param force: 如果旧文档还有内容(或者没有保存),是否要替换?
        """
        if not os.access(path,os.R_OK):
            self.ErrNo = ErrorNum.FileNoFoundErr
            raise NoFoundErr
        if len(self.map.layers)!=0 and not force:
            self.ErrNo = ErrorNum.DocumentNoSaveErr
            raise DocNoSaveErr
        if len(self.map.layers)!=0:
            self.ReInit()
        #file = open(path)
        #docstr = file.read()
        #self.__ParseDocStr(docstr)
        #file.close()
        execfile(path)

    def SaveDocument(self,path):
        """保存当前文档到指定路径(本软件用Python语句作为保存的工程文件)
        @type path: str
        @param path: 保存位置
        """
        docstr = self.__CreateDocStr()
        if not path.endswith(".gsd"):
            path = path+".gsd"
        file = open(path,'w')
        file.write(docstr)
        file.close()

    #def __ParseDocStr(self,string):   

    def __CreateDocStr(self):
        """建立表示文档内容的Python语句
        @rtype: str
        @return: 文档的Python表达
        """
        contextlist = []
        headstr = ""; contextlist.append(headstr)
        importdocstr = "from geosings.ui.core.Document import mainDocument"
        contextlist.append(importdocstr)
        importrectstr = "from geosings.core.GeoRect import GeoRect"
        contextlist.append(importrectstr)
        importlayfstr = "from geosings.core.Layer import LayerFactory"
        contextlist.append(importlayfstr)
        if len(self.map.layers)>0:
            doclayers = createLayers(self.map.layers)
            contextlist.append(doclayers) 
        panstepstr = "mainDocument.panstep=%d" % self.panStep
        contextlist.append(panstepstr)
        if self.geoext is not None:
            rect = self.geoext
            rectarr = [rect.GetLeft(),rect.GetTop(),
                    rect.GetRight(),rect.GetBottom()]
            geoextstr = "mainDocument.geoext=GeoRect(%s)" % (",".join([str(i) for i in rectarr]))
            contextlist.append(geoextstr)
        selections = self.map.GetSelectedLayersItems()
        if len(selections)>0:
            selarrstr = ", ".join([str(i) for i in selections ])
            selstr = "mainDocument.map.SelectLayers([%s])" % selarrstr
            contextlist.append(selstr)
        zoomallstr = "mainDocument.zoomall=%d" % self.zoomall
        contextlist.append(zoomallstr)
        return "\n".join(contextlist)

def createLayers(layers):
    """创建图层内容的文档保存语句
    @type layers: list
    @param layers: 要生成语句的图层列表
    @rtype: str
    @return: 返回表示图层内容的Python语句
    """
    laydocarrs = []
    for layer in layers:
        openlayerstr = """layer = LayerFactory.Open(r'%s')""" % layer.path
        laydocarrs.append(openlayerstr)
        addlayerstr = "mainDocument.map.AddLayer(layer)"
        laydocarrs.append(addlayerstr)
        layvisual = "layer.visual=%d" % layer.visual
        laydocarrs.append(layvisual)
    return "\n".join(laydocarrs)

mainDocument = Document()

