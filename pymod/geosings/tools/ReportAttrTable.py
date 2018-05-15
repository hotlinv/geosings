# -*- coding: utf-8 -*-
"""讲属性表作为HTML报表输出
"""

from geosings.core.Layer import Layer
from geosings.core.DataSet import DataSetType
from ReportHtmlFrame import *
from geosings.core.Exception import *
from geosings.core.system.EncodeTran import *

from time import time
class ReportAttrTable:
    """属性表报表
    """
    def __init__(self,layer):
        """初始化
        @type layer: L{geosings.core.Layer.Layer}
        @param layer: 要做列表报表的图层
        """
        self.layer = layer
        #self.foomap = {DataSetType.Raster:self.__GetRasterTable,
        #        DataSetType.Vector:self.__GetVectorTable}
        self.__GetTable()

    def Report(self):
        """输出报表的HTML内容
        @rtype: str
        @return: 报表HTML内容
        """
        beg = time()
        name = self.__GetName()
        table = self.__GetTabHtml()
        context = '\n'.join([name,
            table])
        print time()-beg
        return context

    def GetTable(self):
        """获取表的头列表和内容列表
        @rtype: list
        @return: 返回两个列表
                    - 表头列
                    - 表值列
        """
        return self.colnames,self.vals

    def __GetName(self):
        """获取图层名
        @rtype: str
        @return: 图层的名称的html表示
        """
        return GetH2(self.layer.name)

    def __GetTable(self):
        """获取表的列表数据
        """
        #dataset = self.layer.DataSet()
        #dslayer = dataset.GetLayer()
        if self.layer.type == DataSetType.Vector:
            dslayer = self.layer.DataSet()
            layerdef = dslayer.GetLayerDefn()
            dslayer.ResetReading()
            self.colnames = ["FID"]
            for i in range(layerdef.GetFieldCount()):
                defn = layerdef.GetFieldDefn(i)
                self.colnames.append(defn.GetName())
            self.vals = []
            f = dslayer.GetNextFeature()
            while(f is not None):
                val = [str(f.GetFID())]
                fs = [astr2utf8(str(f.GetField(i))) for i in range(layerdef.GetFieldCount())]
                    #val.append(str(f.GetField(i)))
                val.extend(fs)
                self.vals.append(val)
                f = dslayer.GetNextFeature()
        else:
            raise UnSupportOperException()
            #print 'raster has no tab!'
    def __GetTabHtml(self):
        """获取表的html表示
        @rtype: str
        @return: 返回表的html表示
        """
        return GetTable(self.colnames,self.vals)

if __name__ == "__main__":
    layer = Layer.Open('e:/gisdata/data/streets.shp')
    ctrl = ReportAttrTable(layer)
    file = open('info.html','w')
    file.write(ctrl.Report())
    file.close()
