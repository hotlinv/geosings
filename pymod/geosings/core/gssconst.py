# -*- coding: utf-8 -*-
"""
该模块是定义geosings中的常量

 - writer:linux_23; create: ; version:1; 创建;
 - linux_23: 2007.5.29; 在SymbolType中添加TEXT类型;
"""

class FeatureType:
    point = 1
    rect = 2

class DataSetType:
    Raster = 2
    Vector = 1
    Unknown = 0

class SymbolType:
    POINT = 1
    LINE = 2
    POLYGON = 3
    TEXT = 4
    UNIQUE = 5

dstStrMap = {
    DataSetType.Raster: 'Raster',
    DataSetType.Vector: 'Vector',
    DataSetType.Unknown: 'Unknown'
}

import ogr,gdal

vextmap = {
        "AVCBin":'*',
        "BNA":"bna",
        "CSV":"csv",
        "DODS":"*",
        "PGeo":"mdb",
        "SDE":"@DB",
        "ESRI Shapefile":"shp",
        "FMEObjects Gateway":"ntf",
        "GeoJSON":"@WEB",
        "Geoconcept":"gxt",
        "GML":"gml",
        "GMT":"gmt",
        "GPX":"gpx",
        "GRASS":"@DIR",
        '"Interlis 1" and "Interlis 2"':"itf/xml/ili",
        "INGRES":"@DB",
        "KML":"kml",
        "MapInfo File":"tab/mif",
        "DGN":"dgn",
        "Memory":"*",
        "MySQL":"@DB",
        "OGDI":"",
        "ODBC":"@DB",
        "OCI":"@DB",
        "PostgreSQL":"@DB",
        "S57":"000",
        "SDTS":"ddf",
        "SQLite":"*",
        "UK .NTF":"ntf",
        "TIGER":"tr1",
        "VRT":"",
        "XPLANE":"dat",
        "IDB":"@DB",
        }

VDSFormatMap = {}
vdcount = ogr.GetDriverCount()
for i in range(vdcount):
    name = ogr.GetDriver(i).GetName()
    if name in vextmap:
        ext = vextmap[name]
    else:
        ext = '*'
    VDSFormatMap[name] = ext

RDSFormatMap = {}
try:
    dlist = [gdal.GetDriver(i) for i in range(gdal.GetDriverCount())]
except:
    dlist = gdal.GetDriverList()
for driver in dlist:
    name = driver.ShortName
    meta = driver.GetMetadata()
    if "DMD_EXTENSION" in meta:
        ext = meta["DMD_EXTENSION"]
    else:
        ext = "*"
    RDSFormatMap[name] = ext

#DSFormatMap = {
#        "GeoTIFF": "tif/tiff", 
#        "Shape file": "shp",
#        "Mapinfo file": "tab/mif",
#        "hdf4/hdf5": "hdf",
#        "PostgreSQL": "",
#        "MySQL" : "",
#        "SQLite" : "db"
#}
DSFormatMap = {}
for k in VDSFormatMap:
    DSFormatMap[k] = VDSFormatMap[k]

for k in RDSFormatMap:
    DSFormatMap[k] = RDSFormatMap[k]
