# -*- coding: utf-8 -*-
"""
该模块定义核心异常

 - writer:linux_23; create: ; version:1; 创建
 - linux_23: 2007.9.7; 添加SQL异常
"""

import geosings.core.system.UseGetText

class ErrorNum:
    """定义异常码和异常消息的名字空间
    """
    NoErr = (0, E("no error"))
    NoOrderErr = (1, E("no found the order"))
    UnSupportOperErr = (2, E("unsupport this operator"))

    FileNoFoundErr = (1000, E("can't find specify file"))
    FileOpenFailuseErr = (1001, E("fail to open file"))
    
    LayerNoFoundErr = (1100, E("no found the layer"))
    UnKnownDataSetErr = (1101, E("unknown dataset format"))
    FieldNoFoundErr = (1102, E("no found the field"))
    
    DocumentNotSaveErr = (1200, E("document no saved"))

    GeomInvalideErr = (1300, E("invalide geometry"))
    SQLInvalideErr = (1301, E("invalide SQL"))

    ToolRunFailErr = (1400, E("run tool failuse"))

    NoMatchErr = (1500, E("datas were not match"))
    SrsNoMatchErr = (1501,E("spatial references were not match"))


class GssException(Exception):
    """该类是geosings的异常类基类
    """
    def __init__(self, errno = ErrorNum.NoErr, errstr = ''):
        self.errno = errno
        self.errstr = errstr
    def GetErrNo(self):
        return self.errno[0]
    def GetExMessage(self):
        return errstr
    def GetMessage(self):
        return self.errno[1]

class NoOrderException(GssException):
    """没有相应命令操作的异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.NoOrderErr, errstr)

class UnSupportOperException(GssException):
    """不支持操作的异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.UnSupportOperErr, errstr)

class UnKnownDataSetException(GssException):
    """未知数据集格式异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.UnKnownDataSetErr, errstr)

class UnOpenDataSetException(GssException):
    """不能打开的数据集异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.FileOpenFailuseErr, errstr)

class FileNotFoundErr(GssException):
    """没有指定文件的异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.FileNoFoundErr, errstr)

class FieldNotFoundErr(GssException):
    """没有指定文件的异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.FieldNoFoundErr, errstr)

class InvalidGeomErr(GssException):
    """几何形状解析异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.GeomInvalideErr, errstr)

class InvalidSQLErr(GssException):
    """SQL语句解析异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.SQLInvalideErr, errstr)

class LayerNoFoundErr(GssException):
    """图层找不到异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.LayerNoFoundErr, errstr)

class DocNoSaveErr(GssException):
    """文档还未保存异常
    """
    def __init__(self,errstr=""):
        GssException.__init__(self, ErrorNum.DocumentNotSaveErr, errstr)

class ToolRunFailErr(GssException):
    """工具运行错误异常
    """
    def __init__(self, errstr=""):
        GssException.__init__(self, ErrorNum.ToolRunFailErr, errstr)

class NoMatchErr(GssException):
    """不匹配错误异常
    """
    def __init__(self, errstr=""):
        GssException.__init__(self, ErrorNum.NoMatchErr, errstr)
class SrsNoMatchErr(GssException):
    """不匹配错误异常
    """
    def __init__(self, errstr=""):
        GssException.__init__(self, ErrorNum.SrsNoMatchErr, errstr)

if __name__=="__main__":
    """测试
    """
    try: raise UnKnownDataSetException()
    except GssException,e: print e.GetMessage()
    try: raise UnOpenDataSetException()
    except GssException,e: print e.GetMessage()
    try: raise FileNotFoundErr()
    except GssException,e: print e.GetMessage()
    try: raise InvalidGeomErr()
    except GssException,e: print e.GetMessage()
    try: raise LayerNoFoundErr()
    except GssException,e: print e.GetMessage()
    try: raise DocNoSaveErr()
    except GssException,e: print e.GetMessage()

