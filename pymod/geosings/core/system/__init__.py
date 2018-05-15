# -*- coding: utf-8 -*-

import os, codecs, sys

__doc__ = '''
这个模块是专门收集作为辅助工具的代码
'''
from EncodeTran import astr2utf8
import UseGetText
#from GLog import *

def choose(bool, a, b):
    '''进行and－or操作的辅助函数，相当于C语言的?:二元操作符
    使用方法 用C语言表示为 (bool)?a:b
    '''
    return (bool and [a] or [b])[0]

def cz_split(aunicode):
    """分割中文和英文字符串
    """
    strs = []
    zh = []
    for i in astr2utf8(aunicode):
        if i>'~':
            if len(zh):
                strs.append("".join(zh))
            zh = []
            strs.append(i)
        else:
            zh.append(i)

    if len(zh):
        strs.append("".join(zh))
    return strs

def GetFileNameNoExt(path):
    '''获取不带扩展名和路径的文件名
    '''
    filename = os.path.basename(path)
    file = os.path.splitext(filename)[0]
    return file

def ScreenPToGeoP(mousex,mousey,scrrect,georect):
    '''通过指定点的屏幕位置计算所在的地理位置
    mousex,mousey 是要计算的点的屏幕坐标
    scrrect 是屏幕的矩形范围
    georect 是屏幕矩形范围所表示的地理范围
    返回值  是计算后的地理坐标x y值
    '''
    gleft = georect.GetLeft()
    gtop = georect.GetTop()
    gwidth = georect.GetWidth()
    gheight = georect.GetHeight()
    dcw = scrrect.GetWidth()
    dch = scrrect.GetHeight()
    geox = gleft+mousex*gwidth*1.0/dcw
    geoy = gtop-mousey*gheight*1.0/dch
    return geox,geoy

def GetThisPath(_file_):
    """获取模块所在的文件夹位置"""
    return os.path.abspath(_file_)

def GetThisDir(_file_):
    '''获取模块所在的文件夹名字'''
    return os.path.split(os.path.abspath(_file_))[0]

def SortedDictValues(adict):
    """排序一个字典"""
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)

def PrintDict(dict):
    """打印一个字典"""
    print "\n".join(["%s=%s" % (k, v) for k, v in dict.items()])

def RandomColorStr():
    """获得一个随机颜色，以#ffffff格式返回"""
    import random
    a = [hex(random.randint(50,205))[2:].rjust(2,'0') for i in range(3)]
    return "#"+"".join(a)

def GetLogicalDriveStrings():
    """win32下获取系统逻辑驱动器名列表，Unix下获取根目录"""
    if os.name == 'nt':
        try:
            from ctypes import windll, c_buffer, c_int32
            L = 256
            divs = c_buffer("\0"*L)
            l = c_int32(L)
            windll.kernel32.GetLogicalDriveStringsA(l,divs)
            return divs.raw.strip("\0").split("\0")
        except:
            from geosings.core.system.DefConf import USERHOME
            dbconf=os.path.join(USERHOME,".divlist")#.divlist文件是列举所有C驱动器外的驱动器
            if not os.access(dbconf, os.F_OK):
                divlist = []
            else:
                f = open(dbconf)
                divlist = []
                line = f.readline().strip()
                while line: 
                    divlist.append(line)
                    line = f.readline().strip()
                f.close()
            return ['c:/']+divlist
    else:
        return ["/"]

def SaveUtf8File(filename, context):
    """写入utf8编码字符串到指定文件中
    @type filename: str
    @param filename: 要保存的文件名
    @type context: str
    @param context: 要写入的内容
    """
    file=codecs.open(filename,'w','utf-8')
    file.write(unicode(context))
    file.close()

def OpenUtf8(filename, flag='r'):
    """打开utf8文件
    """
    return codecs.open(filename,flag,'utf-8')

class MyOutForUIText:
    """把标准输出从控制台重定向到gui的控件中
    """
    def __init__(self, aUITextCtrl,printfun="WriteText"):
        """构造函数
        """
        self.out = aUITextCtrl
        self.pfun = printfun
        sys.stdout = self
        sys.stderr = self
    def write(self, string):
        """替代stdout的write函数，使得print可以直接在控件中打印
        """
        getattr(self.out,self.pfun)(string)
    def ResetStd(self):
        """重新设置回标准控制台打印。
        在使用完控件打印后需要重新设置回标准输出，不然会找不到输出设备。
        """
        sys.stdout=sys.__stdout__
        sys.stderr=sys.__stderr__
    def __del__(self):
        """析构函数，回复用控制台打印
        """
        self.ResetStd()

class ptr:
    def __init__(self,val):
        self.val = val
    def set(self,nval):
        self.val = nval
    def get(self):
        return self.val
    def __eq__(self,oval):
        return self.val==oval

def getptr(val):
    if isinstance(val,ptr):
        return val.get()
    else:
        return val

def ExtGeoRect(rect, width, height):
    """用长宽比来调整第一个矩形形状(中心固定)
    """
    from geosings.core.GeoRect import GeoRect
    rw = rect.GetWidth()
    rh = rect.GetHeight()
    midx, midy = rect.GetMiddlePoint()
    if rw/rh > width*1.0/height:#按宽调整
        newh = height*1.0/width*rw
        neww = rw
    else:#按高调整
        neww = width*1.0/height*rh
        newh = rh
    return GeoRect(midx-neww/2.0,midy+newh/2.0, \
            midx+neww/2.0,midy-newh/2.0)

if __name__=="__main__":
    p = ptr('s')
    p2 = ptr('s')
    p3 = ptr("asdf")
    print p==p2
    print p==p3
    #a={ k.p : "asdf" }
    #p2 = ptr('s')
    #print p2 in a
    print _("Open")

    t = u"我爱python！... I love Python!"
    for i in cz_split(t):print i

    t = "我爱python！".unicode()
    for i in cz_split(t):print i

