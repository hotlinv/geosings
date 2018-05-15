# -*- coding: utf-8 -*-
"""该模块进行坐标的转换
"""
import osr
print 'import osr'

def projcs2geogcs(x,y,wkt):
    """把投影坐标变成地理坐标
    @type x:number
    @type y: number
    @param x,y: 投影坐标点
    @type wkt: str
    @param wkt: 投影坐标的wkt表示
    @rtype: list
    @return: 返回地理坐标经纬度
                - x: 经度
                - y: 纬度
    """
    sr = osr.SpatialReference()
    sr.ImportFromWkt(wkt)
    geogcs = sr.CloneGeogCS()
    ct = osr.CoordinateTransformation(sr,geogcs)
    return ct.TransformPoint(x,y)
    
