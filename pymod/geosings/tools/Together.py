# -*- coding: utf-8 -*-
"""
该模块定义把两个图层合并的操作

 - writer:linux_23; create: 2008.5.15; version:1; 创建
"""
import ogr
from geosings.core.Exception import *
from geosings.core.Layer import *
from geosings.core.system.GLog import *


def together(layer1,layer2):
        ds = layer1.dataSource
        ldefn1 = layer1.GetLayerDefn()
        ldefn2 = layer2.GetLayerDefn()
        if ldefn1.GetGeomType()!=ldefn2.GetGeomType():
            raise NoMatchExcepion
        if layer1.GetSpatialRef() is not None and \
                ( not layer1.GetSpatialRef().IsSame(layer2.GetSpatialRef())):
            raise SrsNoMatchErr
        fdefdict = {}
        for fi in range(ldefn1.GetFieldCount()):
            defn = ldefn1.GetFieldDefn(fi)
            fdefdict[defn.GetName()] = defn
        for fi in range(ldefn2.GetFieldCount()):
            defn = ldefn2.GetFieldDefn(fi)
            fdefdict[defn.GetName()] = defn
        defnns = fdefdict.keys()
        defns = [fdefdict[key] for key in defnns]

        nlayer = CreateVLayer(ds, layer1.GetName()+"_"+layer2.GetName(), \
            layer1.GetSpatialRef(), \
            ldefn1.GetGeomType(), \
            defns)
        ndefn = nlayer.GetLayerDefn()
        feature = layer1.GetNextFeature()
        while feature:
            feat = ogr.Feature(ndefn)
            feat.SetGeometry(feature.GetGeometryRef())
            for fi in range(ldefn1.GetFieldCount()):
                defn = ldefn1.GetFieldDefn(fi).GetName()
                feat.SetField(defn,feature.GetField(defn))
            nlayer.CreateFeature(feat)
            feature = layer1.GetNextFeature()
        feature = layer2.GetNextFeature()
        while feature:
            feat = ogr.Feature(ndefn)
            feat.SetGeometry(feature.GetGeometryRef())
            for fi in range(ldefn2.GetFieldCount()):
                defn = ldefn2.GetFieldDefn(fi).GetName()
                feat.SetField(defn,feature.GetField(defn))
            nlayer.CreateFeature(feat)
            feature = layer2.GetNextFeature()
        nlayer.SyncToDisk()

if __name__=="__main__":
    layer1 = GetLayer("e:/gisdata/china/city","440000",1)
    layer2 = layer1.dataSource.GetLayer("XianCh_point_44")
    together(layer1,layer2)

