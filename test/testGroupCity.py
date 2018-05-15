#-*- encoding:utf-8 -*-
"""测试城市点分组导出
"""
import ogr

from geosings.tools.ExportFeatures import GroupeExportor

def foo(val):
    return val/100*100

datasource = ogr.Open("/gisdata/guangdong/guangdong", 1)
layer = datasource.GetLayer("guangdong2")
GroupeExportor(datasource, layer, "belong",foo)

def foo2(val):
    return val/100*100

datasource2 = ogr.Open("/gisdata/guangdong/city", 1)
layer2 = datasource2.GetLayer("440000_XianCh_point_44")
GroupeExportor(datasource2, layer2, "ADCODE93",foo2)
