# -*- coding: utf-8 -*-
"""
该模块定义全局字典配置

 - writer:linux_23; create: ; version:1; 创建
 - linux_23: 2007.11.27; 添加in自省
"""
import __builtin__

CONFKEY = "geosings_conf"
MSGSKEY = "geosings_key_msgs"

if CONFKEY not in __builtin__.__dict__:
    __builtin__.__dict__[CONFKEY] = {}
    __builtin__.__dict__[CONFKEY][MSGSKEY] = {}

class GssConfDict:
    def __init__(self):
        self.__d = __builtin__.__dict__[CONFKEY]

    def __setitem__(self, key, item):
        self.__d[key] = item

    def __getitem__(self, key):
        try:
            return self.__d[key]
        except:
            return None
    def __contains__(self, key):
        """in方法的自省
        """
        return key in self.__d

GSSCONF = GssConfDict()
GSSMSGS = GSSCONF[MSGSKEY]

GSSCONF["GDALINFO_APP"] = "gdalinfo"
GSSCONF["OGRINFO_APP"] = "ogrinfo"
GSSCONF["OGR2OGR_APP"] = "ogr2ogr"

if __name__ == "__main__":
    GSSCONF["aa"] = "aa"
    GSSCONF["array"] = []
    print GSSCONF["aa"]
    #print __builtin__.__dict__
    GSSCONF["array"].append(12)
    print __builtin__.__dict__[CONFKEY]

    print "pp" in GSSCONF
