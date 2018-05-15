# -*- coding: utf-8 -*-
"""
定义几何形状和WKT的模块
"""

from Exception import InvalidGeomErr
import ogr

def CreatePolygonWkt(points):
    """创建表示多边形的wkt字符串
    @type points: list
    @param points: 一个由(x,y)组合成的队列
    @rtype: str
    @return: 多边形的wkt表示
    """
    if len(points) <3:
        raise 
    pointstxt = ",".join(["%s %s" % (str(p[0]),str(p[1])) for p in points])
    wkt = "POLYGON ((%s))" % pointstxt
    return wkt

def CreatePointWkt(x,y):
    """创建表示点的wkt字符串
    @type x:number
    @type y: number
    @param x,y: 一个由(x,y)表示的点
    @rtype: str
    @return: 点的wkt表示
    """
    return "POINT (%s %s)" % (str(x),str(y))

def CreatePolygon(plist):
    """通过点列表创建多边形
    """
    return ogr.CreateGeometryFromWkt(CreatePolygonWkt(plist))

if __name__=="__main__":
    print CreatePolygon([[1,3],[2,3],[4,6],[7,7]]).ExportToWkt()
