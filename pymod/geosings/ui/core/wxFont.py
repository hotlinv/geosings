# -*- coding: utf-8 -*-
"""该模块进行wx的字体相关封装
 - writer:linux_23; create:2007.6.1 ; version:1; 创建
"""

import wx

class FontUtils:
    """字体工具类，获取字体，或者使用该字体字符串的一些属性
    """
    def __init__(self,font=None,dc=None):
        """用字体来初始化
        """
        from geosings.ui.core.wxSymbol import getFontSymbol 
        if type(font) == dict:#是一个symbol描述
            realfont = getFontSymbol(font)
            self.font = realfont
        else:#是一个wx的字体
            self.font = font
        self.dc = wx.MemoryDC()

    def GetFontSize(self,text):
        """获取使用该字体的字符串的大小
        """
        size = self.dc.GetFullTextExtent(text,self.font)[:2]
        return size

    def __del__(self):
        """销毁
        """
        del self.dc

def GetDefaultFont():
    """获取系统默认字体
    """
    return wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
