# -*- coding: utf-8 -*-
"""
该模块定义导出要素的操作

 - writer:linux_23; create: 2008.4.17; version:1; 创建
"""
import ogr
from geosings.core.Exception import *
from geosings.core.Layer import *
from geosings.core.system.GLog import *
import geosings.core.system.UseGetText

class VOgrLayerSelectionExportor:
    def __init__(self, layer):
        self.layer = layer
    def output(self, selstr, geosel, outdata):
        self.layer.SetAttributeFilter(selstr)
        self.layer.SetSpatialFilter(geosel)
        feature = self.layer.GetNextFeature()
        while feature:
            outdata.CreateFeature(feature)
            feature = self.layer.GetNextFeature()
        outdata.SyncToDisk()
    def filter_output(self, outdata, foo=None, selstr="",  geosel=None):
        self.layer.SetAttributeFilter(selstr)
        self.layer.SetSpatialFilter(geosel)
        feature = self.layer.GetNextFeature()
        while feature:
            if foo is None:
                outdata.CreateFeature(feature)
            elif foo(feature):
                outdata.CreateFeature(feature)
            feature = self.layer.GetNextFeature()
        outdata.SyncToDisk()

def __infoo(foo,fieldname,groupval, f):
    a = foo(f.GetField(fieldname))
    if a==groupval:
        return True
    else:
        return False

def GroupeExportor(datasource, layer, groupefield, foo=None):
    groupvals = []
    ldefn = layer.GetLayerDefn()
    fi = ldefn.GetFieldIndex(groupefield)
    if fi==-1:
        raise FieldNotFoundErr()
    fieldtype = ldefn.GetFieldDefn(fi).GetType()
    isstr = False #是否是字符串
    if fieldtype == ogr.OFTString or \
            fieldtype == ogr.OFTWideString:
        isstr = True
    feature = layer.GetNextFeature()
    while feature:
        val = feature.GetField(groupefield)
        if foo:
            val = foo(val)
        if val not in groupvals:
            groupvals.append(val)
        feature = layer.GetNextFeature()
    for groupval in groupvals:
        info(_('export')+" %s ...", groupval)
        layer.ResetReading()
        ldefn = layer.GetLayerDefn()
        nlayer = CreateVLayer(datasource, str(groupval), \
            layer.GetSpatialRef(), \
            ldefn.GetGeomType(), \
            [ldefn.GetFieldDefn(i) for i in range(ldefn.GetFieldCount())])
        exp = VOgrLayerSelectionExportor(layer)
        if not foo:
            if isstr:
                exp.output(groupefield+"='"+groupval+"'",None,nlayer)
            else:
                exp.output(groupefield+"="+groupval,None,nlayer)
        else:
            exp.filter_output(nlayer, lambda x:__infoo(foo,groupefield,groupval,x))

        info(_("success"))

if __name__=="__main__":
    datasource = ogr.Open("E:/gisdata/china/guangdong", 1)
    layer = datasource.GetLayer("guangdong2")
    GroupeExportor(datasource, layer, "belong")
