#-*- encoding:utf-8 -*-
"""测试用一个图层某属性矫正另一个图层的属性
"""
import ogr
from geosings.core.system.GLog import *
from geosings.core.system.EncodeTran import *

def notify_attr(layer1, layer2, sf1, sf2, nf1, nf2 ):
    fdict = {}
    feature = layer1.GetNextFeature()
    while feature:
        fdict[feature.GetFieldAsString(sf1)[:4]] = feature.GetField(nf1)
        feature = layer1.GetNextFeature()
    feature = layer2.GetNextFeature()
    print '*'*10
    while feature:
        if feature.GetFieldAsString(sf2)[:4] in fdict:
            feature.SetField(nf2, fdict[feature.GetFieldAsString(sf2)[:4]])
            layer2.SetFeature(feature)
        else:
            info(u"no nitify:%s", any2utf8(feature.GetFieldAsString(sf2)))
        feature = layer2.GetNextFeature()
    layer2.SyncToDisk()


datasource = ogr.Open("/gisdata/guangdong/city/440000_XianCh_point_44.shp", 1)
layer1 = datasource.GetLayer()
datasource2 = ogr.Open("/gisdata/guangdong/guangdong/guangdong2.shp")
layer2 = datasource2.GetLayer()
notify_attr(layer2, layer1, "name", "name", "code", "ADCODE93")
