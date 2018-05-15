# -*- coding: utf-8 -*-
"""
该模块定义数据集概念和工具集
"""

import gdal, ogr, os, glob, re
from gdalconst import *
from gssconst import *
from geosings.core.system.GssConfDict import GSSCONF
from geosings.core.system.DefConf import USERHOME
from geosings.core.system import SaveUtf8File, OpenUtf8

def ListFileSysData(path, type='all'):
    """列出文件系统下的所有数据集
    """
    gdalinfo = GSSCONF["GDALINFO_APP"]
    ogrinfo = GSSCONF["OGRINFO_APP"]
    dirpath = os.listdir(path)
    dss=[] ; dirs=[] ; fds=[] ; rds=[]
    #debug( gdalinfo, ogrinfo)
    for files in dirpath:
        p = os.path.join(path,files)
        try:
            if os.path.isfile(p):
                tmpf = os.path.splitext(files)[0]
            else:
                tmpf = files
            if tmpf in dss:
                raise
            type = None
            dsinfo = os.popen(r'%s "%s"' % (gdalinfo,p))
            infoline = dsinfo.readline()
            dsinfo.close()
            del dsinfo
            if infoline.startswith("Driver:"):
                type = "raster"
                rds.append(files)
                dss.append(tmpf)
                continue
            else:
                cmd = r'%s "%s"' % (ogrinfo,p)
                #debug(cmd)
                dsinfo = os.popen(cmd)
                infoline = dsinfo.readline()
                dsinfo.close()
                del dsinfo
                if not infoline.startswith("FAILURE:"):
                    type = "feature"
                    fds.append(files)
                    dss.append(tmpf)
                    continue
                else:
                    raise
        except:
            if os.path.isdir(p):
                dirs.append(tmpf)
    return fds,rds,dirs


class DBConfManager:
    def __init__(self,dbtype):
        self.dbtype = dbtype
        self.__GetDBConf()
        self.__GetDBConfArray()

    def GetDBTypes():
        confs = glob.glob(os.path.join(USERHOME,".dbconf.*"))
        types = []
        for conf in confs:
            tmp = conf.split(".")
            types.append( tmp[len(tmp)-1])
        return types
    GetDBTypes = staticmethod(GetDBTypes)

    def GetDBConfFilePath(self):
        return os.path.join(USERHOME,".dbconf."+self.dbtype.lower())

    def __GetDBConf(self):
        #self.dbconffile=dbconf=os.path.join(USERHOME,".dbconf."+self.dbtype)
        self.dbconffile=dbconf=self.GetDBConfFilePath()
        if not os.access(dbconf, os.F_OK):
            SaveUtf8File(dbconf, u"regs:")

    def __GetDBConfArray(self):
        f=OpenUtf8(self.dbconffile)
        self.dbconfarray = []
        line = f.readline().strip()
        while line: 
            self.dbconfarray.append(line)
            line = f.readline().strip()
        f.close()
        self.GetDBList()

    def GetDBList(self):
        if getattr(self,"dblist",None) is None:
            f = OpenUtf8(self.dbconffile)
            line = f.readline().strip()
            f.close()
            tmplist = line.split(":")
            if len(tmplist)==0 or tmplist[1]=="":
                self.dblist = []
            else:
                self.dblist = tmplist[1].split(",")
        return self.dblist

    def Add(self,name,host,dbname,user,pwd):
        self.dblist = dblist = self.GetDBList()
        if name in dblist: 
            raise "already has same name dbreg"
        dblist.append(name)
        self.dbconfarray[0] = "regs:" + ",".join(dblist)
        self.dbconfarray.append("%s:host:%s" % (name, host))
        self.dbconfarray.append("%s:dbname:%s" % (name, dbname))
        self.dbconfarray.append("%s:user:%s" % (name, user))
        self.dbconfarray.append("%s:password:%s" % (name, pwd))
        self.__WriteFile()

    def Edit(self,name,host,dbname,user,pwd):
        self.dblist = dblist = self.GetDBList()
        if name not in dblist: 
            raise "have no this dbreg"
        self.dbconfarray = [i for i in self.dbconfarray if not i.startswith(name)]
        self.dbconfarray.append("%s:host:%s" % (name, host))
        self.dbconfarray.append("%s:dbname:%s" % (name, dbname))
        self.dbconfarray.append("%s:user:%s" % (name, user))
        self.dbconfarray.append("%s:password:%s" % (name, pwd))
        self.__WriteFile()

    def __WriteFile(self):
        #f = open(self.dbconffile,'w')
        #f.write("\n".join(self.dbconfarray))
        #f.close()
        debug("write to file")
        SaveUtf8File(self.dbconffile, unicode("\n".join(self.dbconfarray)))

    def Delete(self,name):
        dblist = self.GetDBList()
        if name not in self.dblist:
            raise "no dbreg to delete"
        self.dblist = [i for i in dblist if i!=name]
        self.dbconfarray = [i for i in self.dbconfarray if not i.startswith(name)]
        self.dbconfarray[0]= "regs:" + ",".join(self.dblist)
        self.__WriteFile()

    def IsRegExist(self,name):
        return name in self.GetDBList()

    def GetInfos(self,name):
        info = {"dbname":"", "host":"", "user":"", "password":""}
        if name not in self.dblist:
            return info
        else:
            for i in self.dbconfarray:
                if i.startswith(name):
                    tmp = i.split(":")
                    info[tmp[1]]=tmp[2]
        return info

    def __GetPGConnStr(self,name):
        infos = self.GetInfos(name)
        items = infos.items()
        str = ["%s=%s" % (i[0],i[1]) for i in items]
        return 'PG:"%s"' % " ".join(str)

    def __GetMySQLConnStr(self,name):
        infos = self.GetInfos(name)
        items = infos.items()
        if infos["password"] == "": pwd = ""
        else: pwd = ",password="+infos["password"]
        constr = "MYSQL:"+infos["dbname"]+",user="+infos["user"]+pwd
        debug("MySqlConn:",constr)
        return constr

    def GetConnectStr(self, name=None):
        if self.dbtype.lower()==u"PostgreSQL".lower() or \
                self.dbtype.lower()=="PostgreSQL".lower():
            return self.__GetPGConnStr(name)
        elif self.dbtype.lower()==u"MySQL".lower() or \
                self.dbtype.lower()=="MySQL".lower():
            return self.__GetMySQLConnStr(name)
        else:
            raise "no this db:"+str(name)


def ListDBSysData(conn, type="all"):
    gdalinfo = GSSCONF["GDALINFO_APP"]
    ogrinfo = GSSCONF["OGRINFO_APP"]
    dbinfof = os.popen('%s %s' % (ogrinfo, conn))
    subnames = []
    restr = r"^\d+:\s(.+)\s\(.+\)$"
    line = dbinfof.readline().strip()
    while line: 
        m = re.match(restr, line)
        if m is not None:
            gs = m.groups()
            subnames.append("DB@"+conn+":"+gs[0])
        line = dbinfof.readline().strip()
    return subnames,[],[]
#class DataSetInfo

