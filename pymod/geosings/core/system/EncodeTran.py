# -*- coding: utf-8 -*-
"""
该模块定义数据图层概念。并且定义具体数据类型图层


 - decode是解码(把字符串以什么的方式解析)
 - encode是编码(转换)
"""
import locale

syslocale = locale.getdefaultlocale()


def getcodename(s):
    if type(s) == unicode:
        return "utf-8"

    encodestr = ["utf-8","cp936"]
    for i in encodestr:
        try:
            s.decode(i)
            return i
        except:
            pass

def any2utf8(o):
    if type(o)==unicode or type(o)==str:
        return astr2utf8(o)
    else:
        return unicode(o)

def astr2utf8(s):
    #print type(s)
    if type(s) == unicode:
        return s
    try:
        return s.decode('utf-8')
    except:#pass
        return s.decode('cp936').encode('utf-8').decode('utf-8')

def utf82locale(s):
    #print type(s)
    if type(s) == unicode:
        return s.encode(syslocale[1])
    return s.decode('utf-8').encode(syslocale[1])

def decode2locale(s):
    return s.decode(syslocale[1])
#if syslocale[0]=='zh_CN':
#    print 'locale is', syslocale[1]
#    from geosings.core.locales.ErrMapUTF8 import *
#    if syslocale[1] != 'utf-8':
#        for i in ErrorMap.keys():
#            ErrorMap[i] = ErrorMap[i].decode('utf-8').encode(syslocale[1])
#else:
#    from geosings.core.locales.ErrMapEN import *
def astr2sth(s,enc):
    #print type(s)
    if type(s) == unicode:
        return s.encode(enc)
    try:
        return s.decode('utf-8').encode(enc)
    except:#pass
        return s.decode('cp936').encode(enc)


if __name__ == "__main__":
    i = u"试试看"
    print getcodename(astr2sth(i,'gbk'))
    print getcodename(astr2sth(i,'utf-8'))
    print astr2utf8(i)
    print type("试试看")
    i = "试试看".decode('utf-8').encode('gbk')
    print 'e',getcodename(i)
    print getcodename(astr2sth(i,'gbk'))
    print getcodename(astr2sth(i,'utf-8'))
    print astr2utf8("看看")
    print astr2utf8(i)

    i = u"试试看"
    print 'e',getcodename(i)
    print utf82locale(i)
    i = u"试试看"
    print i, type(i), i.encode('gbk')
    print utf82locale(i)

    print '*'*20


