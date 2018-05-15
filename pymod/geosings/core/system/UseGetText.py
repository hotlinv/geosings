# -*- coding: utf-8 -*-
"""
该模块进行本地化定义(包括界面和错误提示)

 - writer:linux_23; create: ; version:1; 创建
"""

from GssConfDict import GSSCONF

if GSSCONF["LOCALE"]:
    SYS_LC = GSSCONF["LOCALE"]
else:
    import locale
    SYS_LC = locale.getdefaultlocale()[0]

import __builtin__
if "_" not in __builtin__.__dict__:
    import gettext,os,DefConf
    cn_Path = os.path.join(DefConf.MODHOME,'locale',SYS_LC,'geosings.mo')
    if os.access(cn_Path,os.F_OK):
        cat = gettext.GNUTranslations(open(cn_Path,'rb'))
        __builtin__.__dict__["_"]=cat.ugettext
    else:
        __builtin__.__dict__["_"]=unicode

if "E" not in __builtin__.__dict__:
    import gettext,os,DefConf
    e_Path = os.path.join(DefConf.MODHOME,'locale',SYS_LC,'gsserr.mo')
    if os.access(e_Path,os.F_OK):
        cat = gettext.GNUTranslations(open(e_Path,'rb'))
        __builtin__.__dict__["E"]=cat.ugettext
    else:
        __builtin__.__dict__["E"]=unicode


if __name__=="__main__":
    print _("Exit")
