# -*- coding: utf-8 -*-
"""
管理Tools的配置。包括读取用户配置。

 - writer:linux_23; create: 2007.8.16; version:1; 创建
"""

from geosings.core.system.GssConfDict import GSSCONF
from geosings.core.system.GLog import *

def regTool(name,oper):
    if GSSCONF["GSS_TOOLS_OPER"] is None : 
        GSSCONF["GSS_TOOLS_OPER"] = {}
    GSSCONF["GSS_TOOLS_OPER"][name] = oper
    return name

def regToolMenu(patharr,toolname):
    if GSSCONF["GSS_TOOLS_CONF"] is None : 
        GSSCONF["GSS_TOOLS_CONF"] = [] 
    tmp = GSSCONF["GSS_TOOLS_CONF"]
    tmp2 = None
    for path in patharr:
        isin = False
        for i in tmp:
            if path in i:
                isin = True
        if not isin:
            tmp.append({path:[]})
        tmp2 = tmp
        tmp = tmp[len(tmp)-1][path]
    tmp.append({toolname:GSSCONF['GSS_TOOLS_OPER'][toolname]})

_r2v = regTool("Raster To VRML","Raster2VrmlUI")
_o2m = regTool("Ogr to MySQL","Ogr2ogr4intoMySQLUI")
_o2pg = regTool("Ogr to PostgresSQL","Ogr2ogr4intoPGUI")
_sras = regTool("Split Raster","RasterSplitterUI")
_rr = regTool("Resize Raster","RasterResizerUI")
_el = regTool("Export Layer's Info",'ReportLayerInfoUI')
_epgsr = regTool("Export PostGIS SpatialReference","PostGISSrsExpUI")
_scs = regTool("Set coordinate system to dataset","SetCoorSysUI")
_prj = regTool("Project","ProjectUI")
_intersection = regTool("Intersection","IntersectionUI")
_clip = regTool("Clip","ClipUI")

#debug(GSSCONF["GSS_TOOLS_OPER"])

GTM_DATACONV = "Data Convertor"
GTM_DATAOPER = "Data Operator"
GTM_REPORT = "Report"
GTM_SR = "SpatialReference"
GTM_OVERLAY = "Overlay"

regToolMenu([GTM_DATACONV], _r2v)
regToolMenu([GTM_DATACONV], _o2m)
regToolMenu([GTM_DATACONV], _o2pg)
regToolMenu([GTM_DATAOPER], _sras)
regToolMenu([GTM_DATAOPER], _sras)
regToolMenu([GTM_REPORT], _el)
regToolMenu([GTM_SR], _epgsr)
regToolMenu([GTM_SR], _scs)
regToolMenu([GTM_SR], _prj)
regToolMenu([GTM_OVERLAY], _intersection)
regToolMenu([GTM_OVERLAY], _clip)

debug(GSSCONF["GSS_TOOLS_CONF"])

#GSSCONF["GSS_TOOLS_CONF"] = [
#    {"Data Convertor":[
#        {"Raster to VRML":"Raster2VrmlUI"},
#        {"Ogr to MySQL":"Ogr2ogr4intoMySQLUI"},
#        {"Ogr to PostgresSQL":"Ogr2ogr4intoPGUI"},
#        ]
#    },
#    {"Data Operator":[
#        {"Split Raster":"RasterSplitterUI"},
#        {"Resize Raster":"RasterResizerUI"}
#        ]
#    },
#    {"Report":[
#        {"Export Layer's Info":'ReportLayerInfoUI'}
#        ]
#    },
#    {"SpatialReference":[
#        {"Export PostGIS SpatialReference":"PostGISSrsExpUI"},
#        {"Set coordinate system to dataset":"SetCoorSysUI"},
#        {"Project":"ProjectUI"},
#        ]
#    }
#]
