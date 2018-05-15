# -*- coding: utf-8 -*-
"""
该模块进行wkb二进制的解析
"""

import struct,Numeric,sys,ogr
from geosings.core.system import choose

endian_name = sys.byteorder

wkbXDR = '>'     # Big Endian
wkbNDR = '<'     # Little Endian

BTOR = choose(endian_name == 'little',wkbNDR,wkbNDR)

def up_endian_type(wkb):
    """解析字节顺序
    @type wkb: binary str
    @param wkb: 要解析的二进制wkb
    @rtype: list
    @return: 返回一个列表
                - endian 字符串表达字节顺序
                - wkbtype wkb所表示的类型
                - endian_t 系统字节类型，表示字节顺序
    """
    endian_t = struct.unpack('b',wkb[0])[0]
    endian = choose(endian_t,'<','>')
    wkbtype = struct.unpack(endian+'I',wkb[1:5])[0]
    return endian,wkbtype,endian_t

def up_len(wkb,beg,endian):
    return struct.unpack(endian+'I',wkb[beg:beg+4])[0]

def up_point(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    points = Numeric.array(struct.unpack(endian+"2d",wkb[5:]))
    return points

def up_linestring(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    lenght = up_len(wkb,5,endian)
    #points = array('d',wkb[9:9+lenght*16])
    points = Numeric.fromstring(wkb[9:9+lenght*16],Numeric.Float)
    if endian != BTOR : points = points.byteswapped()
    return points

def up_linearring(wkb,ringcount,endian):
    #endian,wkbtype,et = up_endian_type(wkb)
    points = []
    ptr = 0
    for i in range(ringcount):
        length = up_len(wkb,ptr,endian)
        #ps = array('d',wkb[ptr+4:ptr+4+length*16])
        ps = Numeric.fromstring(wkb[ptr+4:ptr+4+length*16],Numeric.Float)
        if endian != BTOR : ps = ps.byteswapped()
        points.append(ps)
        ptr += 4+length*16
    return points,ptr

def up_polygon(wkb,sub=-1):
    endian,wkbtype,et = up_endian_type(wkb)
    if sub == -1:
        ringcount = up_len(wkb,5,endian)
        points = up_linearring(wkb[9:],ringcount,endian)[0]
        return points
    else:
        points = []
        ptr = 5
        ringcount = up_len(wkb,ptr,endian)
        ps,ringlen = up_linearring(wkb[ptr+4:],ringcount,endian)
        points.append(ps)
        ptr += 4+ringlen
        return points,ptr

def up_mpoint(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    subcount = up_len(wkb,5,endian)
    points = []
    ptr = 9
    for i in range(subcount):
        subps = up_point(wkb[ptr:])
        points.append(subps)
        ptr += 9+len(subps)*8
    return points

def up_mlinestring(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    subcount = up_len(wkb,5,endian)
    points = []
    ptr = 9
    for i in range(subcount):
        subps = up_linestring(wkb[ptr:])
        points.append(subps)
        ptr += 9+len(subps)*8
    return points 

def up_mpolygon(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    subcount = up_len(wkb,5,endian)
    points = []
    ptr = 9
    for i in range(subcount):
        subps,size = up_polygon(wkb[ptr:],i)
        points.append(subps)
        ptr += size
    return points 

fun_map = {
        ogr.wkbPoint : up_point,
        ogr.wkbLineString : up_linestring,
        ogr.wkbPolygon : up_polygon,
        ogr.wkbMultiPoint : up_mpoint,
        ogr.wkbMultiLineString : up_mlinestring,
        ogr.wkbMultiPolygon : up_mpolygon
        }

def WkbUnPacker(wkb):
    endian,wkbtype,endian_t = up_endian_type(wkb)
    foo = fun_map[wkbtype]
    points = foo(wkb)
    return [endian_t,wkbtype,points]


if __name__ == "__main__":
    import time
    ds = ogr.Open("/home/share/gisdata/data/streets.shp")
    layer = ds.GetLayer()
    begt = time.time()
    #count = layer.GetFeatureCount()
    #count  = 2
    feature = layer.GetNextFeature()
    #for i in [1]:#range(count):
    while feature is not None:
        #feature = layer.GetFeature(i)
        geom = feature.GetGeometryRef()
        #print geom.ExportToWkt()
        wkb = geom.ExportToWkb()
        wkbarr = WkbUnPacker(wkb)
        feature = layer.GetNextFeature()
        #if wkbarr[1] > 3:
        #    print wkbarr
    print time.time()-begt
