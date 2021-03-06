﻿# -*- coding: utf-8 -*-
"""
该模块定义获取ui所需要的函数
"""
import wx,os

from geosings.core.system import *
from geosings.core.system.DefConf import *
from geosings.core.system.GssConfDict import GSSCONF

def GetImageDirPath():
    """获取图像文件夹路径
    @rtype: str
    @return: 图像文件夹的路径
    """
    thisdir = GetThisDir(__file__)
    parentdir = os.path.split(thisdir)[0]
    return os.path.join(parentdir,"image")

def GetStyleDirPath():
    """获取样式文件夹路径
    @rtype: str
    @return: 样式文件夹的路径
    """
    thisdir = GetThisDir(__file__)
    parentdir = os.path.split(thisdir)[0]
    return os.path.join(parentdir,"styles")

def GetMainIcon():
    """获取主程序的图标
    @rtype: wxICON
    @return: 主程序的图标对象
    """
    icondir = GetImageDirPath()
    iconpath = os.path.join(icondir,'geosings.ico')
    return wx.Icon(iconpath,wx.BITMAP_TYPE_ICO)

def GetSplashBitmap():
    """获取闪屏的图片
    @rtype: wxBitmap
    @return: 闪屏上使用的图片
    """
    bmpdir = GetImageDirPath()
    bmppath = os.path.join(bmpdir,'geosings.png')
    #bmppath = os.path.join(bmpdir,'toucan.png')
    img = wx.Bitmap(bmppath, wx.BITMAP_TYPE_ANY)
    #img.ConvertAlphaToMask(220)
    return img

def GetBitmapByName(name,bmpdir=GetStyleDirPath()):
    bmppath = os.path.join(bmpdir, name)
    return wx.Bitmap(bmppath, wx.BITMAP_TYPE_ANY)

def GetRasterSymbol(name='rassym',width=30,height=20):
    """获取栅格样式图标
    @rtype: wxBitmap
    @return: 相应图标
    """
    imgdir = GetImageDirPath()
    bmppath = os.path.join(imgdir,name+'.gif')
    if os.access(bmppath,os.F_OK):
        image = wx.Image(bmppath,wx.BITMAP_TYPE_ANY)
    else:
        try:
            image = wx.Image(os.path.join(imgdir,'unknown.gif'),wx.BITMAP_TYPE_ANY)
        except:
            image = wx.EmptyImage(width,height)
    image.Rescale(width,height)
    return image.ConvertToBitmap()

def GetToolBarImg(name,isdef=True):
    """获取工具栏图标
    @type name: str
    @param name: 工具栏图标名
    @rtype: wxBitmap
    @return: 相应图标
    """
    imgdir = GetImageDirPath()
    bmppath = os.path.join(imgdir,name+'.gif')
    if os.access(bmppath,os.F_OK):
        image = wx.Image(bmppath,wx.BITMAP_TYPE_ANY)
    else:
        try:
            image = wx.Image(os.path.join(imgdir,'unknown.gif'),wx.BITMAP_TYPE_ANY)
        except:
            image = wx.EmptyImage(GSSCONF["TOOLBAR_BITMAP_WIDTH"],
                    GSSCONF["TOOLBAR_BITMAP_HEIGHT"])
    image.Rescale(GSSCONF["TOOLBAR_BITMAP_WIDTH"],
            GSSCONF["TOOLBAR_BITMAP_HEIGHT"])
    return image.ConvertToBitmap()

def GetFormatImageList():
    """获取各种数据格式的图标列表
    """
    index = {}
    il = wx.ImageList(16, 16)
    bmpdir = GetImageDirPath()
    sbmp = wx.Bitmap(os.path.join(bmpdir,'source.jpg'), wx.BITMAP_TYPE_ANY)
    index['source'] = il.Add(sbmp)
    dirbmp = wx.Bitmap(os.path.join(bmpdir,'dir.jpg'), wx.BITMAP_TYPE_ANY)
    index['dir'] = il.Add(dirbmp)
    fbmp = wx.Bitmap(os.path.join(bmpdir,'feature.jpg'), wx.BITMAP_TYPE_ANY)
    index['feature'] = il.Add(fbmp)
    rbmp = wx.Bitmap(os.path.join(bmpdir,'raster.jpg'), wx.BITMAP_TYPE_ANY)
    index['raster'] = il.Add(rbmp)
    dbbmp = wx.Bitmap(os.path.join(bmpdir,'database.jpg'), wx.BITMAP_TYPE_ANY)
    index['database'] = il.Add(dbbmp)
    return il,index
