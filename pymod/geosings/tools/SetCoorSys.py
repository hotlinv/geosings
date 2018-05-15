# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.6.29; version:1; 创建
"""
该模块定义投影设置功能
"""
import osr,os
from geosings.core.gssconst import *
from geosings.core.Layer import Layer

def SetCoorSys(layer, sr, opath):
    """为图层设置投影
    @type layer: Layer
    @param layer: 要设置投影的图层
    @type sr: ogr.SpatialReference
    @param sr: 要设置的坐标系
    @type opath: str 
    @param opath: 要输出的图层位置 
    """
    if layer.type==DataSetType.Raster:
        name = layer.name
        dataset = layer.DataSet()
        driver = dataset.GetDriver()
        filename = name
        meta = driver.GetMetadata()
        if 'DMD_EXTENSION' in meta:
            if meta["DMD_EXTENSION"] != "":
                filename = '.'.join([name,meta['DMD_EXTENSION']])
        filename = os.path.join(opath,filename)
        newds = driver.CreateCopy(filename, dataset, 0)
        newds.SetProjection(sr.ExportToWkt())
    elif layer.type==DataSetType.Vector:
        name = layer.name
        dataSource = layer.dataSource
        dataset = layer.DataSet()
        driver = dataSource.GetDriver()
        newds = driver.CreateDataSource(opath)
        layer2 = newds.CreateLayer(name,sr)
        lu = LayerUtil(layer)
        lu.CopyDataset(layer2)
        newds.Destroy()
    
def SetCoorSysByWkt(layer, wkt, opath):
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
    SetCoorSys(layer,sr, opath)
    

if __name__=="__main__":
    from geosings.core.system.EncodeTran import utf82locale
    layer = Layer.Open(utf82locale(u"J:/gisdata/GTIF/ping1.tif"))
    sr = osr.SpatialReference()
    sr.SetWellKnownGeogCS("WGS84")
    SetCoorSys(layer, sr, 'd:/gisdata')
