# -*- coding: utf-8 -*-
"""
该模块是定义地理的矩形对象。

 - writer:linux_23; create: ; version:1; 创建
 - linux_23; 2007.11.13; 添加RectExt
 - linux_23; 2008.4.13; 添加Set方法
"""

from geosings.core.system import * 

class Rect:
    """定义普通类型的矩形模型
    """
    def __init__(self,x1,y1,w,h):
        """构造函数
        @type x1:int
        @type y1: int
        @param x1,y1: 左上角点的xy坐标
        @type w: int
        @param w: 矩形的宽
        @type h: int
        @param h: 矩形的高
        """
        self.ReSet(x1,y1,w,h)
    def ReSet(self,x1,y1,w,h):
        """重新设置整个矩形"""
        self.__left = x1
        self.__top = y1
        self.__right = x1+w
        self.__bottom = y1+h
        self._w = w
        self._h = h

    def GetLeft(self):
        """获取最左端的点的X坐标
        @rtype: int
        @return: 最左端的X坐标
        """
        return self.__left
    def GetRight(self):
        """获取最右端的点的X坐标
        @rtype: int
        @return: 最右端的X坐标
        """
        return self.__right
    def GetTop(self):
        """获取最上端的Y坐标
        @rtype: int
        @return: 最上端的Y坐标
        """
        return self.__top
    def GetBottom(self):
        """获取最底端的Y坐标
        @rtype: int
        @return: 最底端的Y坐标
        """
        return self.__bottom
    def GetWidth(self):
        """获取矩形宽
        @rtype: int
        @return: 矩形宽
        """
        return self._w
    def GetHeight(self):
        """获取矩形高
        @rtype: int
        @return: 矩形高
        """
        return self._h
class GeoRect:
    """定义地理的矩形范围
    """
    def __init__(self,x1,y1,x2,y2):
        """构造函数
        @type x1:number
        @type y1: number
        @param x1,y1: 第一个点的xy坐标
        @type x2:number
        @type y2: number
        @param x2,y2: 第二个点的xy坐标
        """
        self.ReSet(x1,y1,x2,y2)
    def __str__(self):
        """定义打印格式"""
        return 'l:%.3f,r:%f,t:%f,b:%f\n(W:%f,H:%f)' % \
                (self.__left,self.__right,self.__top,self.__bottom, \
                self.GetWidth(),self.GetHeight())
    def GetLeft(self):
        """获取最左边的坐标"""
        return self.__left
    def SetLeft(self,left):
        """设置最左边的坐标"""
        right = self.__right
        self.__left = choose(left<right,left,right)
        self.__right = choose(left>right,left,right)
    def GetRight(self):
        """获取最右边的坐标"""
        return self.__right
    def SetRight(self,right):
        """设置最右边的坐标"""
        left = self.__left
        self.__left = choose(left<right,left,right)
        self.__right = choose(left>right,left,right)
    def GetTop(self):
        """获取最上边的坐标"""
        return self.__top
    def SetTop(self,top):
        """设置最上边的坐标"""
        bottom = self.__bottom
        self.__top = choose(top<bottom,bottom,top)
        self.__bottom = choose(top>bottom,bottom,top)
    def GetBottom(self):
        """获取最下边的坐标"""
        return self.__bottom
    def SetBottom(self,bottom):
        """设置最下边的坐标"""
        top = self.__top
        self.__top = choose(top<bottom,bottom,top)
        self.__bottom = choose(top>bottom,bottom,top)
    def GetWidth(self):
        """获取宽度"""
        return self.__right-self.__left
    def GetHeight(self):
        """获取高度"""
        return self.__top-self.__bottom
    def GetMiddlePoint(self):
        """获取中间点"""
        midx = (self.__left+self.__right)/2.0
        midy = (self.__top+self.__bottom)/2.0
        return midx,midy
    def ReSet(self,x1,y1,x2,y2):
        """重新设置整个矩形"""
        self.__left = choose(x1<x2,x1,x2)
        self.__right = choose(x1>x2,x1,x2)
        self.__top = choose(y1<y2,y2,y1)
        self.__bottom = choose(y1>y2,y2,y1)
    def Set(self, rect):
        """根据另一个GeoRect来进行设置
        """
        self.__left = rect.__left
        self.__right = rect.__right
        self.__top = rect.__top
        self.__bottom = rect.__bottom

class RectExt:
    """定义一个根据数个矩形计算所有矩形外包范围的类
    """
    def __init__(self):
        """定义矩形的上下左右边范围
        """
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
    def AddRect(self, rect):
        """往范围内添加一个矩形，并计算新的范围
        """
        if self.left is None:
            self.left = rect.GetLeft()
            self.right = rect.GetRight()
            self.top = rect.GetTop()
            self.bottom = rect.GetBottom()
            return
        if rect.GetLeft()<left:
            self.left = rect.GetLeft()
        if rect.GetRight()>right:
            self.right = rect.GetRight()
        if rect.GetTop()>top:
            self.top = rect.GetTop()
        if rect.GetBottom()<bottom:
            self.bottom = rect.GetBottom()
    def GetExt(self):
        """获取所有矩形的外包范围
        """
        if self.left is None:
            self.left = 0
            self.right = 0
            self.top = 0
            self.bottom = 0
        return GeoRect(self.left, self.top, self.right, self.bottom)

import ogr
def GetGeoRectGeometry(rect):
    """把GeoRect转化成Wkt字符串表示形式"""
    wkt = "POLYGON ((%f %f,%f %f,%f %f,%f %f,%f %f))" % \
            ( rect.GetLeft(), rect.GetTop(),
              rect.GetLeft(), rect.GetBottom(),
              rect.GetRight(), rect.GetBottom(),
              rect.GetRight(), rect.GetTop(),
              rect.GetLeft(), rect.GetTop())
    return ogr.CreateGeometryFromWkt(wkt)

