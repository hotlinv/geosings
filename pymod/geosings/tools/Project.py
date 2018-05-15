# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.6.29; version:1; 创建
"""
该模块定义投影转换工具
"""
import osr,os
import geosings.core.system.UseGetText
from geosings.core.gssconst import *
from geosings.core.Layer import *

def conv_fun(x,y):
    return x+0.01,y+0.01

def Project(layer, sr, opath):
    """为图层设置投影
    @type layer: Layer
    @param layer: 要设置投影的图层
    @type sr: ogr.SpatialReference
    @param sr: 要设置的坐标系
    @type opath: str 
    @param opath: 要输出的图层位置 
    """
    if layer.type==DataSetType.Raster:
        pass
    elif layer.type==DataSetType.Vector:
        name = layer.name
        dataSource = layer.dataSource
        dataset = layer.DataSet()
        if dataset.GetSpatialRef() is None:
            print E('data has no spatilref info')
            return
        driver = dataSource.GetDriver()
        newds = driver.CreateDataSource(opath)
        layer2 = newds.CreateLayer(name,sr)

        ct = osr.CoordinateTransformation(dataset.GetSpatialRef(),sr)
        lu = LayerUtil(layer)
        lu.ConvertXYs(lambda x,y: ct.TransformPoint(x,y)[:2],layer2)

        newds.Destroy()
    
def ProjectByWkt(layer, wkt, opath):
    """为图层设置投影
    @type layer: Layer
    @param layer: 要设置投影的图层
    @type wkt: str
    @param wkt: 要设置的坐标系wkt表示
    @type opath: str 
    @param opath: 要输出的图层位置 
    """
    sr = osr.SpatialReference()
    sr.ImportFromWkt(wkt)
    Project(layer,sr, opath)
    

if __name__=="__main__":
    from geosings.core.system.EncodeTran import utf82locale
    layer = OpenV(utf82locale(u"/gisdata/xm/xm.shp"))
    sr = osr.SpatialReference()
    file = open("/linux_23/geosings/srs/srs/Beijing 1954.prj")
    sr.ImportFromWkt(file.read())
    file.close()
    #sr.SetWellKnownGeogCS("WGS84")
    Project(layer, sr, '/gisdata/xm1')
