# -*- coding: utf-8 -*-

"""
该模块定义把数据导入MySQL的工具的UI定义
"""
import os
from geosings.core.Exception import *
from geosings.core.system.GssConfDict import GSSCONF
from geosings.core.system.EncodeTran import utf82locale

class Ogr2ogr4intoMySQL:
    def __init__(self,layerpath,connstr):
        self.layerpath = layerpath
        self.connstr = connstr
        self.engine = None
        self.rename = None
        self.overwrite = None
        self.spatialIndex = None
        self.update = None
    def SetEngine(self, engine):
        self.engine = engine
    def SetNewName(self, newName):
        self.rename = newName
    def SetOverWrite(self, overwrite=True):
        self.overwrite = overwrite
    def SetBuildSpatialIndex(self, build=True):
        self.spatialIndex = build
    def SetUpdate(self, update=True):
        self.update = update

    def Run(self):
        ogr2ogr = utf82locale(GSSCONF["OGR2OGR_APP"])
        keymap = []
        createopts = []
        if self.engine is not None:
            createopts.append("ENGINE="+self.engine)
        if not self.spatialIndex:
            createopts.append("SPATIAL_INDEX=NO")
        if self.rename is not None:
            keymap.append("-nln "+self.rename)
        if self.overwrite:
            keymap.append("-overwrite")
        if self.update:
            keymap.append("-update")
        lco = ""
        if len(createopts) >0:
            lco = " -lco "+" ".join(createopts)
        command = " ".join([ogr2ogr, " -f MySQL ",self.connstr,self.layerpath, \
            " ".join(keymap), lco])
        print command
        r = os.system(command)
        if r != 0:
            raise ToolRunFailErr(_("error"))

class Ogr2ogr4intoPG:
    """ogr2ogr -f PostgreSQL PG:"dbname=geodb user=postgres password=postgres" G:\gisdata\china\BOUNT_line.shp
    """
    def __init__(self,layerpath,connstr):
        self.layerpath = layerpath
        self.connstr = connstr

    def Run(self):
        ogr2ogr = utf82locale(GSSCONF["OGR2OGR_APP"])
        command = " ".join([ogr2ogr," -f PostgreSQL ",self.connstr,self.layerpath])
        print command
        r = os.system(command)
        if r != 0:
            raise ToolRunFailErr(_("error"))

if __name__=="__main__":
    from geosings.core.RunSysConf import RunSysConf
    RunSysConf()#使得ogr2ogr的使用路径生效，如果不用特殊设置，就用默认的
    tool = Ogr2ogr4intoMySQL("e:/gisdata/shp/lines.shp", 
            "MYSQL:geo,user=root,password=mysql")
    tool.SetUpdate()
    tool.SetOverWrite()
    tool.SetNewName("lines2")
    tool.SetEngine("MyISAM")
    tool.Run()
