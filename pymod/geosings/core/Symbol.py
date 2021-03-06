# -*- coding: utf-8 -*-
"""
绘制样式配置类

 - writer:linux_23; create: ; version:1; 创建
 - linux_23: 2007.5.29; 添加Text默认类型
"""
from gssconst import *
import ogr
from geosings.core.system import RandomColorStr
from geosings.core.system.GLog import *
from geosings.core.system.GssConfDict import GSSCONF

#class Symbol:
#    """要素绘制时的样式配置
#    """
#    Type = SymbolType.POINT
#    Color = "#000000"
#    Size = 1
#    OutlineColor = "#000000"

PointSymConfKeys = ['size','color']
"""点型样式可以设置的关键字
"""
def CreatePointSymbol(color):
    """创建简单点的样式
    返回一个字典共包含下面内容
    type:一定是SymbolType.POINT
    size:点大小，默认是2
    color:点颜色，默认是随机颜色
    """
    debug('PointSymbol')
    return {'type':SymbolType.POINT,
            'size':2,
            'color':color}

LineSymConfKeys = ['size','color']
"""线型样式可以设置的关键字
"""
def CreateLineSymbol(color):
    """创建简单线的样式
    返回一个字典共包含下面内容
    type:一定是SymbolType.LINE
    size:线宽，默认是1
    color:线颜色，默认是随机颜色
    """
    debug('lineSymbol')
    return {'type':SymbolType.LINE,
            'size':1,
            'color':color}

PolygonSymConfKeys = ['size','color','olcolor']
"""多边形样式可以设置的关键字
"""

def CreatePolygonSymbol(color):
    """创建简单多边形的样式
    返回一个字典共包含下面内容
    type:一定是SymbolType.POLYGON
    size:外边线线宽，默认是1
    color:填充颜色，默认是随机颜色
    olcolor:外边线颜色，默认是随机颜色
    """
    debug('PolygonSymbol')
    return {'type':SymbolType.POLYGON,
            'size':1,
            'color':color,
            'olcolor':RandomColorStr()}

UniqueSymConfKeys = ['size','field','colormap','olcolor','ramp']
"""唯一值样式可以设置的关键字
"""
from geosings.core.ColorRamp import ColorRamp
def CreateUniqueSymbol(field):
    """创建简单多边形的样式
    返回一个字典共包含下面内容
    type:一定是SymbolType.POLYGON
    size:外边线线宽，默认是1
    field:要归类的字段
    ramp:从中取的颜色带
    color:填充颜色，默认是从ramp中取出的随机颜色
    olcolor:外边线颜色，默认是随机颜色
    """
    debug('UniqueSymbol')
    return {'type':SymbolType.UNIQUE,
            'size':1,
            'field':field,
            'ramp':ColorRamp(name='urainbow'),
            'colormap':{},
            'olcolor':RandomColorStr()}

TextSymConfKeys = ['font','size','bcolor','bold','color']
"""文字样式可以设置的关键字
"""

def CreateTextSymbol():
    """创建字体的样式
    返回一个字典共包含下面内容
    type: 一定是SymbolType.POLYGON
    font: 字体，默认是宋体
    size: 字体大小，默认是16
    """
    return {"type": SymbolType.TEXT,
            'font': "宋体",
            'size': 9,
            #'bcolor': "#ffffaa",
            #'bold': False,
            }

GetDefPointSymbol = CreatePointSymbol
GetDefLineSymbol = CreateLineSymbol
GetDefPolygonSymbol = CreatePolygonSymbol
GetDefTextSymbol = CreateTextSymbol

def CreateSymbol(symbolType):
    """根据类型创建颜色
    """
    if symbolType == ogr.wkbPoint or \
        symbolType == ogr.wkbMultiPoint:
        return GetDefPointSymbol(RandomColorStr())
    elif symbolType == ogr.wkbLineString or \
        symbolType == ogr.wkbMultiLineString:
        return GetDefLineSymbol(RandomColorStr())
    elif symbolType == ogr.wkbPolygon or \
        symbolType == ogr.wkbMultiPolygon:
        return GetDefPolygonSymbol(RandomColorStr())
    elif symbolType == "text" or \
        symbolType == "SymbolType:"+str(SymbolType.TEXT):
        return GetDefTextSymbol()

def CreateHLSymbol(symbolType):
    """根据类型创建高亮颜色
    """
    selectcolor = GSSCONF["HL_COLOR"]
    if symbolType == ogr.wkbPoint or \
        symbolType == ogr.wkbMultiPoint:
        return GetDefPointSymbol(selectcolor)
    elif symbolType == ogr.wkbLineString or \
        symbolType == ogr.wkbMultiLineString:
        return GetDefLineSymbol(selectcolor)
    elif symbolType == ogr.wkbPolygon or \
        symbolType == ogr.wkbMultiPolygon:
        return GetDefPolygonSymbol(selectcolor)
