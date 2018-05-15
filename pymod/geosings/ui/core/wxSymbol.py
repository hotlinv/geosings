# -*- coding: utf-8 -*-
"""该模块进行Symbol模块的覆盖

 - writer:linux_23; create:2007.4.5; version:1; 创建
 - linux_23; 2007.6.1; 添加字体相关函数
 - linux_23; 2007.11.28; 添加透明颜色支持
"""

import wx,binascii,struct
from geosings.core.Symbol import *
from geosings.ui.core.wxFont import GetDefaultFont
from geosings.ui.core.MainImage import GetBitmapByName
from geosings.core.system import RandomColorStr
from geosings.core.ColorRamp import rainbow

def getSelectSymbol(sytype):
    return {}
def split4ColorStr(colorstr):
    try:
        return struct.unpack("4B",binascii.a2b_hex(colorstr))
    except:
        return (0,0,0,0)

def join42ColorStr(r,g,b,a=None):
    if a is None:
        return "#%02x%02x%02x" % (r,g,b)
    else:
        return "#%02x%02x%02x%02x" % (r,g,b,a)

def COLORSTR(color):
    """把任何形式Color变成#ffffffff这种格式
    """
    if type(color)==str or type(color)==unicode:
        return color
    elif type(color)==list or type(color)==tuple:
        if len(color)==3:
            return join42ColorStr(color[0],color[1],color[2])
        else:
            return join42ColorStr(color[0],color[1],color[2],color[3])
def COLOR(color):
    """把任何形式变成wx的Colour格式
    """
    if type(color)==str or type(color)==unicode:
        if color.startswith('#'):
            if len(color)==7:
                return wx.NamedColour(color)
            elif len(color)==9:
                carr = split4ColorStr(color[1:])
                return wx.Colour(carr[0],carr[1],carr[2],carr[3])
        elif color.upper().startswith("RGBA"):
            c = eval(color[4:])
            if len(c)!=4:
                return wx.BLACK
            elif max(c)>255 or min(c)<0:
                return wx.BLACK
            else:
                return wx.Colour(c[0],c[1],c[2],c[3])
        elif color.upper().startswith("RGB"):
            return wx.NamedColour(color)
        else:
            return wx.BLACK
    else:
        return color
def getPanSymbol(symbol):
    """获取Symbol的笔样式
    """
    symtype = symbol['type']
    if symtype==SymbolType.POINT:
        return wx.NullPen
    elif symtype==SymbolType.LINE:
        color = COLOR(symbol['color'])
    elif symtype==SymbolType.POLYGON:
        color = COLOR(symbol['olcolor'])
    else:
        return wx.NullPen
    if 'hatch' in symbol:
        style = symbol['hatch']
    else:
        style = wx.SOLID
    size = symbol['size']
    pen = wx.Pen(color,size,style)
    return pen


def getBrushSymbol(symbol, fieldval=None):
    """获取Symbol的画刷样式
    """
    symtype = symbol['type']
    if symtype==SymbolType.POINT:
        color = COLOR(symbol["color"])
        brush = wx.Brush(color)
        return brush
    elif symtype==SymbolType.LINE:
        color = COLOR(symbol["color"])
        brush = wx.Brush(color)
        return brush
    #return wx.NullBrush
    elif symtype==SymbolType.POLYGON:
        if 'bitmap' in symbol:
            brush = wx.NullBrush
            brush.SetStipple(GetBitmapByName(symbol['bitmap']))
            brush.SetStyle(wx.STIPPLE)
        elif 'hatch' in symbol:
            brush = wx.NullBrush
            brush.SetStyle(symbol['hatch'])
            if 'color' in symbol:
                brush.SetColour(COLOR(symbol['color']))
        elif 'color' in symbol:
            if symbol['color'] is None:
                return wx.TRANSPARENT_BRUSH
            brush = wx.Brush(COLOR(symbol['color']))
        return brush
    elif symtype==SymbolType.UNIQUE:
        if fieldval in symbol['colormap']:
            color = COLOR(symbol['colormap'][fieldval])
            brush = wx.Brush(color)
            return brush
        else:
            #colors = symbol['colormap'].values()
            #colorstr = RandomColorStr()
            #while colorstr in colors:
            #    colorstr = RandomColorStr()
            #symbol['colormap'][fieldval]=colorstr
            color = symbol['ramp'].random_color()
            color = COLOR(color)
            #print color
            symbol['colormap'][fieldval]=COLORSTR(color)
            brush = wx.Brush(color)
            return brush
    pass

def getSizeSymbol(symbol):
    """获取Symbol的大小样式
    """
    if 'size' in symbol:
        return symbol['size']
    else:
        return 0

def getFontSymbol(symbol):
    """获取Symbol的字体样式
    """
    font = GetDefaultFont()
    if "font" in symbol:
        font.SetFaceName(symbol["font"])
    if "size" in symbol:
        font.SetPointSize(int(symbol['size']))
    if "blod" in symbol:
        if symbol["blod"]:
            font.SetWeight(wx.FONTWEIGHT_BOLD)
    return font

def getFontBColorSymbol(symbol):
    """获取Symbol的字体背景颜色
    """
    if 'bcolor' in symbol:
        return COLOR(symbol["bcolor"])
    else:
        return None
def getFontFColorSymbol(symbol):
    """获取Symbol的字体颜色
    """
    if 'color' in symbol:
        return COLOR(symbol["color"])
    else:
        return None

if __name__=="__main__":
    wx.App()
    symbol = CreateSymbol(1)
    pan = getPanSymbol(symbol)
    brush = getBrushSymbol(symbol)
    print pan,brush

    print COLOR("#00ffdd12")
    print COLOR("#4c4052")
    print COLOR("RGBA(122,44,33,22)")
    print COLOR("RGBA(122,44,33)")
    print COLOR("RGB(122,44,33)")
    print COLOR("rgb( 22, 44, 77)")
