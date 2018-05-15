#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
进行叠加分析的操作

 - writer:linux_23; create: Wed Nov 14 21:11:55 2007 ; version:1; 创建
"""

import ogr,os
from geosings.core.gssconst import *
from geosings.core.Layer import Layer,LayerUtil
from geosings.core.DefConf import USERHOME

def CreateNewLayer(opath,name,ogrlayer,rename=0):
    layerdef = ogrlayer.GetLayerDefn()
    #print dir(layerdef)
    driver = ogr.GetDriverByName("ESRI Shapefile")
    if not name.endswith(".shp"):
        oname=name+".shp"
    else:
        oname=name
    outputfile = os.path.join(opath,oname)
    if os.access( outputfile, os.F_OK ):
        driver.DeleteDataSource( outputfile )
    newds = driver.CreateDataSource(outputfile)
    layernew=newds.CreateLayer(name,None,layerdef.GetGeomType())
    #需要拷贝Field，不然不会考虑属性数据
    if rename:
        fidField=ogr.FieldDefn(ogrlayer.GetName()+"_"+"FID",ogr.OFTInteger)
        layernew.CreateField(fidField)
    for i in range(layerdef.GetFieldCount()):
        fielddef = layerdef.GetFieldDefn(i)
        if rename:
            fielddef.SetName(ogrlayer.GetName()+"_"+fielddef.GetName())
        layernew.CreateField(fielddef)
    return layernew,newds

def GeoSplit(layer,rename=0):
    """把几何形状分解成不互相压制的要素集
    """
    opath=USERHOME
    name="tmp.shp"
    name2="tmp2.shp"
    dsoper = layer.DataSet()
    newlayer,newds = CreateNewLayer(opath,name,dsoper)
    f = dsoper.GetNextFeature()
    while f is not None:
        newlayer.CreateFeature(f)
        f = dsoper.GetNextFeature()
    dsoper.ResetReading()
    features = []
    f2 = dsoper.GetNextFeature()
    while f2 is not None:
        g = f2.GetGeometryRef()
        newlayer.ResetReading()
        f3 = newlayer.GetNextFeature()
        iscross=0
        while f3 is not None:
            g2 = f3.GetGeometryRef()
            if g.Intersect(g2) and not g.Equal(g2):
                dg = g.Difference(g2)
                ig = g.Intersection(g2)
                f4 = f3.Clone()
                f5 = f3.Clone()
                f4.SetGeometry(dg)
                f5.SetGeometry(ig)
                features.append(f4)
                features.append(f5)
                iscross = 1
                #newlayer.GetNextFeature()
            f3 = newlayer.GetNextFeature()
        if not iscross:
            features.append(f2)
        f2 = dsoper.GetNextFeature()
    newlayer2,newds2 = CreateNewLayer(opath,name2,dsoper,rename)
    for f in features:
        newlayer2.CreateFeature(f)
    newlayer2.SyncToDisk()
    #newds2.Destroy()
    newds.Destroy()
    return newlayer2

def Clip(layerTag,layerOper,opath,name):
    """截取分析
    """
    #创建一个空的几何形状集合来放操作图层的几何集合
    ngcoll = ogr.CreateGeometryFromWkt("GEOMETRYCOLLECTION EMPTY")
    
    dsoper = layerOper.DataSet()
    f = dsoper.GetNextFeature()
    if f is not None:
        l2gcoll = f.GetGeometryRef()
        #print l2gcoll.ExportToWkt()
        #f.Destroy()
        f3 = dsoper.GetNextFeature()
        while f3 is not None:
            g = f3.GetGeometryRef()
            #print g.ExportToWkt()
            l2gcoll = g.Union(l2gcoll)
            #l2gcoll.AddGeometry(g)
            #f.Destroy()
            f3 = dsoper.GetNextFeature()
    else:
        return
    
    #print l2gcoll.ExportToWkt()
    dstag = layerTag.DataSet()
    newlayer,newds = CreateNewLayer(opath,name,dstag)
    f2 = dstag.GetNextFeature()
    while f2 is not None:
        g2 = f2.GetGeometryRef()
        gopered = g2.Intersection(l2gcoll)
        if not gopered.Equal(ngcoll):
            f2.SetGeometry(gopered)
            newlayer.CreateFeature(f2)
        f2.Destroy()
        f2 = dstag.GetNextFeature()
    newds.Destroy()

def Intersection(layerTag,layerOper,opath,name):
    """相交分析
    """
    #创建一个空的几何形状集合来放操作图层的几何集合
    ngcoll = ogr.CreateGeometryFromWkt("GEOMETRYCOLLECTION EMPTY")
    
    #dsopertmp = layerOper.DataSet()
    dsoper = GeoSplit(layerOper)
    
    #print l2gcoll.ExportToWkt()
    dstag = layerTag.DataSet()
    newlayer,newds = CreateNewLayer(opath,name,dstag,1)

    operdef = layerOper.DataSet().GetLayerDefn()
    fidField=ogr.FieldDefn(layerOper.name+"_"+"FID",ogr.OFTInteger)
    newlayer.CreateField(fidField)
    for i in range(operdef.GetFieldCount()):
        fielddef = operdef.GetFieldDefn(i)
        fielddef.SetName(layerOper.name+"_"+fielddef.GetName())
        newlayer.CreateField(fielddef)
    #newdef = newlayer.GetLayerDefn()
    #for i in range(newdef.GetFieldCount()):
    #    fielddef = newdef.GetFieldDefn(i)
    #    print fielddef.GetName()
    operDefn = layerOper.DataSet().GetLayerDefn()
    tagDefn = layerTag.DataSet().GetLayerDefn()

    f2 = dstag.GetNextFeature()
    while f2 is not None:
        g2 = f2.GetGeometryRef()
        dsoper.ResetReading()
        f3 = dsoper.GetNextFeature()
        while f3 is not None:
            g3 = f3.GetGeometryRef()
            gopered = g2.Intersection(g3)
            if not gopered.Equal(ngcoll):
                #print gopered.ExportToWkt()
                fnew = ogr.Feature(newlayer.GetLayerDefn())
                fnew.SetGeometry(gopered)
                fnew.SetField(layerTag.DataSet().GetName()+"_FID",f2.GetFID())
                fnew.SetField(layerOper.DataSet().GetName()+"_FID",f3.GetFID())
                for ofi in range(tagDefn.GetFieldCount()):
                    fielddef = tagDefn.GetFieldDefn(ofi)
                    nfn = fielddef.GetName()
                    fnew.SetField(nfn,f2.GetField(ofi))
                for ofi in range(operDefn.GetFieldCount()):
                    fielddef = operDefn.GetFieldDefn(ofi)
                    nfn = fielddef.GetName()
                    fnew.SetField(nfn,f3.GetField(ofi))
                newlayer.CreateFeature(fnew)
            f3 = dsoper.GetNextFeature()
        f2.Destroy()
        f2 = dstag.GetNextFeature()
    newds.Destroy()

if __name__== "__main__":
    layer = Layer.Open("I:/geosings/pymod/geosings/core/3D/line.shp")
    layer2 = Layer.Open("I:/geosings/pymod/geosings/core/3D/bound.shp")
    Intersection(layer,layer2,'i:/gisdata/output','intersect')
    #GeoSplit(layer2)
