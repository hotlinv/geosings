# -*- encoding: utf-8 -*-

"""该模块运行系统的配置文件
"""

from DefConf import USERHOME
from GssConfDict import GSSCONF, GSSMSGS
import os

def RunSysConf():
    #from GLog import info
    rcname = os.path.join(USERHOME,'.gssrc')
    if not os.access(rcname,os.F_OK):
        rcname = os.path.join(USERHOME,'_gssrc')
    print 'using rc file:',rcname

    if os.access(rcname,os.F_OK):
        execfile(rcname)

