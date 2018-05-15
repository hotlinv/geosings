# -*- coding: utf-8 -*-
"""
该模块定义命令的处理函数的对应列表

 - writer:linux_23; create: ; version:1; 创建
 - linux_23: 2007.5.29; 添加标注命令
 - linux_23: 2007.6.14; 修改管理类，添加设置函数，移除标志设置到UISettings中
"""

from geosings.core.system.GssConfDict import GSSMSGS,GSSCONF

#class keyptr(ptr):
#    def __init__(self,manager,name,val):
#        self.manager = manager
#        self.name = name
#        self.val = val

#    def get(self):
#        return getattr(self.manager,self.name)

#    def set(self,nval):
#        self.manager.SetMsgKey(self.name,nval)

class MsgManager:
    """所有Geosings主程序的命令的集合管理类
    """
    def __init__(self):
        self.__MsgKeyMap = {}
        #self.ptrs = {}

    def SetKeyMap(self, key, order, foo=None):
        GSSMSGS[key] = order
        if foo is not None:
            self.__MsgKeyMap[key] = foo

    def GetKeyMap(self):
        oMsgKeyMap = {}
        for key in self.__MsgKeyMap:
            oMsgKeyMap[GSSMSGS[key]]=self.__MsgKeyMap[key]
        return oMsgKeyMap
    #def GetKeyPtr(self,keyname):
    #    if keyname not in dir(self):
    #        return 
    #    kptr = keyptr(self,keyname,getattr(self,keyname))
    #    self.ptrs[keyname] = kptr
    #    return kptr

    #def SetMsgKey(self, keyName,keyVal,foo=None):
    #    if keyName not in dir(self):#添加
    #        if foo is None:#添加不能不定义函数
    #            print _('fail to set MsgKey function'),':',keyVal,'=>None'
    #            return
    #        setattr(self,keyName,keyVal)
    #        self.__MsgKeyMap[keyVal] = foo
    #        return
    #    okeyVal = getattr(self,keyName)
    #    if foo is None:
    #        if okeyVal in self.__MsgKeyMap:
    #            foo = self.__MsgKeyMap[okeyVal]
    #        else:
    #            foo = None
    #    if okeyVal in self.__MsgKeyMap:
    #        self.__MsgKeyMap.pop(okeyVal)
    #    setattr(self,keyName,keyVal)
    #    self.__MsgKeyMap[keyVal] = foo
    #    if keyName in self.ptrs:
    #        kptr = self.ptrs[keyName]
    #        kptr.val = keyVal

def ReInitMsgWordMap():
    #只能初始化一次
    mwm = GSSCONF["MSGKEY"] = MsgManager()
    return mwm

if __name__=="__main__":
    #mm = MsgManager()
    #mm.SetMsgKey('MSG_KEY_OPEN',':add')
    #def printtt():
    #    print 'tt'
    #mm.SetMsgKey('MSG_KEY_TT',':tt',printtt)
    #print mm.GetKeyMap()
    pass
