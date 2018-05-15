# -*- coding: utf-8 -*-
"""
该模块是进行路径，命令，参数的补齐操作.
 
 - writer:linux_23; create: ; version:1; 创建
 - linux_23: 2007.9.10; 修改命令补齐方式，自动从MSG的字典中读取
"""

import os
import re
from GLog import *
from GssConfDict import GSSMSGS


class FillLine:
    '''该类是进行路径，命令，参数的补齐操作'''
    def __init__(self,layers = [], orders = None):
        '''初始化补全列表
        @type layers: list
        @param layers: 图层名队列
        @type orders: list
        @param orders: 命令名队列'''
        self.layers = layers
        self.SetOrders(orders)

    def SetLayers(self,layers):
        '''初始化图层补全对象
        @type layers: list
        @param layers: 图层名队列'''
        self.layers = layers

    def SetOrders(self,orders):
        '''初始化命令补全对象
        @type orders: list 
        @param orders: 命令名队列'''
        self.orders = orders

    def __GetType(self,line):
        '''获取补全类型，看是命令补全还是图层补全还是路径补全
        line:是未完整的内容
        返回:获取补全的方法'''
        pathmatch = r'("?(\w:)?([\\/][^\\/:*?"<>|]*)+)$'
        ordmatch = r'^:[\w\S]*$'
        laymatch = r'([lL]\[\w[\w\s]*)$'
        if re.match(ordmatch, line) is not None:
            return self.__GetOrder
        if len(re.findall(pathmatch,line))>0:
            return self.__GetPath
        if len(re.findall(laymatch, line))>0:
            return self.__GetLayer
        else:
            return None
    
    def GetLine(self,line):
        '''获取补全的整行，这是对外的主要接口
        @type line: str
        @param line: 是未补全的内容
        @rtype: str
        @return: 完整的内容'''
        foo = self.__GetType(line)
        if foo is None:
            debug('no any match to fill line!')
            return line
        else:
            return foo(line)

    def __GetPath(self,line):
        '''补全路径，分割多个路径，然后调用__OsPath来补全
        line 是未补全的内容
        返回 完整的路径'''
        if line.count('"') % 2:
            parts = line.split('"')
            path = self.__OsPath(parts[-1])
            newline = '"'.join(['"'.join(parts[0:-1]),path])
        else:
            parts = line.split(' ')
            path = self.__OsPath(parts[-1])
            newline = ' '.join([' '.join(parts[0:-1]),path])
        return newline
        #return self.__OsPath(path, SYSSIGN)

    def __GetOrder(self,partord):
        '''补全命令
        partord 是未补全的命令
        返回 完整的命令'''
        partord2 = partord.lower()

        if self.orders:
            orders = self.orders
        elif GSSMSGS:
            orders = GSSMSGS.values()
            orders.sort()
        else:
            orders = []

        if partord2 == ":" and orders and len(orders)>0:
            return orders[0]
        
        same = 0
        for i in orders:
            if not i.startswith(":"):
                continue
            if same:
                partord = i
                break
            if i.lower().startswith(partord2):
                if i.lower() == partord2:
                    same = 1
                    continue
                partord = i
                break

        return partord

    def __GetLayer(self,line):
        '''补全图层的名字
        line 是未补全的图层名
        返回 完整的图层名'''
        restr = r'^(:[\w\S]+.+)([lL]\[)([\w\s]*)$'
        m = re.match(restr,line)
        if m is None:
            return line
        ord,h,ln = m.groups()
        ln = ln.lower()
        fullname = ''
        for i in self.layers:
            fnamel = i.name.lower()
            if fnamel.startswith(ln): 
                if fullname == '' or len(i.name)<len(fullname):
                    fullname = i.name
        line = ord + fullname
                
        #return re.sub(r'[lL]\[','',line)
        return line

    def __OsPath(self,path):
        '''补全路径
        line 是未补全的内容
        返回 完整的路径'''
        restr = r'(.*[\\/])([^:*?"<>|]*)$'
        #at = path.rfind(sign)
        m = re.match(restr,path)
        if m is None:
            debug(path,'can not match!')
            return path
        dirpath,partfile = m.groups()
        #debug(dirpath,partfile)
        #dirpath,partfile = path[0:at+1],path[at+1:]
        try:
            #os.chdir(dirpath)
            childs = os.listdir(dirpath)
            childs.sort()
            dirpathl = dirpath.lower()
            partfilel = partfile.lower()
            for i in range(len(childs)):
                childl = childs[i].lower()
                if childl.startswith(partfilel):
                    if childl!=partfilel:
                        filename = childs[i]
                        return "".join([dirpath,filename])
                    else:
                        if i!=len(childs)-1:
                            filename = childs[i+1]
                            return "".join([dirpath,filename])
                        else:
                            filename = childs[0]
                            return "".join([dirpath,filename])
            return path
        except Exception ,args:
            return path

fillline = FillLine()

if __name__ == "__main__":
    fl = FillLine([],[":select"])
    print fl.GetLine("/")
    print fl.GetLine("/ho")
    print fl.GetLine("/home/sh")
    print fl.GetLine("/home/share")
    print fl.GetLine("/home/share/")
    print fl.GetLine("/home/share/")
    print fl.GetLine(":sel")
