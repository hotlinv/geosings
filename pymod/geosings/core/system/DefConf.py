# -*- coding: utf-8 -*-
"""
定义默认设置的模块。

计算了HOME，DOC，BIN的路径
"""

import os
import re

def GetUserHomePath():
    """获取用户HOME目录，如果在UNIX下，就是用户目录，
    在windows下，如果有设HOME环境变量就是在环境变量下，如果没有设置就是默认用户目录
    @rtype: str
    @return: 用户目录位置
    """
    bapath = os.path.expanduser("~")
    uhpath = os.path.join(bapath,".geosings")
    if os.access(uhpath,os.F_OK) and os.path.isdir(uhpath):
        return uhpath
    elif os.access(uhpath,os.F_OK) and os.path.isfile(uhpath):
        uhpath = os.path.join(bapath,".gsshome")
        os.makedirs(uhpath)
        return uhpath
    else:
        os.makedirs(uhpath)
        return uhpath

def GetHOMEPATH():
    """获得GSS_HOME的路径
    @rtype: str
    @return: 返回GSS_HOME的路径
    """
    thispath = os.path.abspath(__file__)# get the module path!
    #print thispath
    #print dir(),__file__,__name__,os.path
    #hpmatch = r"(.+([\\/]geosings)+)(([\\/])\w+)+([\\/]geosings[\\/].+){1}"
    #m = re.match(hpmatch, thispath)
    #if m is not None:
    #    #print m.groups()
    #    gs = m.groups()
    #    return gs[0],gs[3]
    #else:
    #    return 're match false','/'
    hpmatch,f = os.path.split(thispath)
    other = None
    while 1:
        hpmatch,other = os.path.split(hpmatch)
        if other=='pymod': break
    return hpmatch,os.path.sep

#系统路径标识符
SYSSIGN = '/'

GSSHOME,SYSSIGN = GetHOMEPATH()
DOCHOME = os.path.join(GSSHOME,'docs')
BINHOME = os.path.join(GSSHOME,'bin')
MODHOME = os.path.join(GSSHOME,'pymod','geosings')
USERHOME = GetUserHomePath()

if __name__ == '__main__':
    print GSSHOME,SYSSIGN,DOCHOME,BINHOME,MODHOME,USERHOME
