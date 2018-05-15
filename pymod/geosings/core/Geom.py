# -*- coding: utf-8 -*-
"""
定义几何形状的操作

 - writer:linux_23; create: 2007.6.6; version:1; 创建
"""


import struct,Numeric,ogr,math
import sys as msys

endian_name = msys.byteorder

wkbXDR = '>'     # Big Endian
wkbNDR = '<'     # Little Endian
from geosings.core.system import choose

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

def make_endian_type(wkbtype):
    """封装字节顺序
    """
    endian_t = choose(BTOR=="<",1,0)
    return struct.pack(BTOR+'bI', endian_t, wkbtype)

def make_point(x, y):
    """做点的wkb
    """
    bin = struct.pack(BTOR+"2d",x,y)
    return make_endian_type(ogr.wkbPoint)+bin

def make_linestring(points):
    """做线的wkb
    """
    length = len(points)
    lenbin = struct.pack(BTOR+"I",length)
    if type(points) == Numeric.array:
        data = points
    else:
        data = Numeric.array(points,Numeric.Float)
    return make_endian_type(ogr.wkbLineString)+lenbin+ \
            data.tostring()

def make_linearring(points):
    length = len(points)
    lenbin = struct.pack(BTOR+"I",length)
    if type(points) == Numeric.array:
        data = points
    else:
        data = Numeric.array(points,Numeric.Float)
    return lenbin+data.tostring()

def make_polygon(rings):
    """做多边形的wkb
    """
    length = len(rings)
    lenbin = struct.pack(BTOR+"I",length)
    h = make_endian_type(ogr.wkbPolygon)+lenbin
    ringarr = []
    for r in rings:
        ringarr.append(make_linearring(r))
        #h+=make_linearring(r)
    return h+"".join(ringarr)
    
def CreateLineString(plist):
    return ogr.CreateGeometryFromWkb(make_linestring(plist))

def CreatePolygon(plist):
    """通过点列表创建多边形
    """
    return ogr.CreateGeometryFromWkb(make_polygon([plist]))

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

def CacLineLen(p1,p2):
    """获得线段长度
    """
    return math.sqrt(math.pow(p1[0]-p2[0],2)+math.pow(p1[1]-p2[1],2) )

class LineStringParser:
    def __init__(self, linepoints):
        if linepoints.__class__ == ogr.Geometry:
            self.line = []
            for i in range(linepoints.GetPointCount()):
                self.line.append([linepoints.GetX(i),linepoints.GetY(i)])
        else:
            self.line = linepoints
        lens = []
        last = None
        for i in self.line:
            if last is not None:
                lens.append(CacLineLen(i,last))
            last = i
        self.tlen = 0
        for i in lens: self.tlen+=i
        self.lens = lens
    
    def GetMidPoint(self):
        halflen = self.tlen/2.0
        tmplen = 0
        i = 0
        while tmplen<halflen:
            tmplen+=self.lens[i]
            i+=1
        xlen = tmplen-halflen
        return GetPointOnLineByDist(self.line[i],self.line[i-1],xlen)  

    def GetMidPart(self):
        at = int(len(self.lens)/2)
        return self.line[at],self.line[at+1]

    def GetLongestPart(self):
        maxlen = max(self.lens)
        at = self.lens.index(maxlen)
        return self.line[at], self.line[at+1]

    def GetLen(self):
        return self.tlen

def GetPointOnLineByDist(p2,p1,dist):
    """在一根线段上取靠近第一点的距离dist的点位置
    @type p2: point
    @param p2: 线段的起始点
    @type p1: point
    @param p1: 线段的终止点
    @type dist: number
    @param dist: 距离位置（必须大于零）
    """
    assert(dist>0)#距离必须大于零
    if p1[0]==p2[0]:
        y = choose(p2[1]>p1[1],p2[1]-dist,p2[1]+dist)
        return p1[0],y
    K = (p1[1]-p2[1])/float((p1[0]-p2[0]))
    Q = float(p1[1]-p2[1]-K*p1[0])
    M = (dist*dist-p2[0]*p2[0]-Q*Q)/(K*K+1)
    T = (K*Q-p2[0])/(K*K+1)
    x1 = math.sqrt(M+T*T)-T
    x2 = -math.sqrt(M+T*T)-T
    y1 = K*(x1-p1[0])+p1[1]
    y2 = K*(x2-p1[0])+p1[1]
    #print p2,p1,x1,y1,x2,y2,(p2[0]-p1[0]),(p2[0]-x1),(p2[1]-p1[1]),(p2[1]-y1)
    if ((p2[0]-p1[0])*(p2[0]-x1)>=0) and \
            ((p2[1]-p1[1])*(p2[1]-y1)>=0):
        return x1,y1
    else: return x2,y2

def ScaleLineByMidPoint(p1,p2,length):
    midx,midy = (p1[0]+p2[0])/2.0, (p1[1]+p2[1])/2.0
    #print midx,midy
    halfLen = length/2.0
    return GetPointOnLineByDist([midx,midy],p1,halfLen), \
            GetPointOnLineByDist([midx,midy],p2,halfLen)

def SplitLine(p1,p2,steplist):
    """分割一条线段，返回分割后的点列表
    """
    split_len = len(steplist)+1
    lineLen = CacLineLen(p1,p2)
    realLen = 0
    for i in steplist: realLen+=i
    #print realLen
    
    p1,p2 = ScaleLineByMidPoint(p1,p2,realLen)
    #print p1,p2,"*"
    lineLen = realLen
    
    stepDist = float(lineLen)/split_len
    ret = []
    dist = stepDist
    for i in range(split_len-1):
        ret.append(GetPointOnLineByDist(p1,p2,dist))
        dist += stepDist
    return ret
    

if __name__ == "__main__":
    print GetPointOnLineByDist([30,30],[30,0],12)
    geomp = make_point(32.2, 133.5)
    print ogr.CreateGeometryFromWkb(geomp).ExportToWkt()
    geomp2 = make_linestring([[1,3],[2,4],[3,4],[4,7]])
    ogrline = ogr.CreateGeometryFromWkb(geomp2)
    print ogrline.GetGeometryCount()
    print ogr.CreateGeometryFromWkb(geomp2).ExportToWkt()
    geomp3 = make_polygon([[[1,3],[2,4],[3,4],[4,7]]])
    ogrpl = ogr.CreateGeometryFromWkb(geomp3)
    print ogrpl.GetGeometryCount()
    print ogrpl.ExportToWkt()
    geom4 = CreatePolygon([[1,3],[2,4],[3,4],[4,7]])
    print geom4.ExportToWkt()

    lp = LineStringParser(ogrline)
    print lp.lens
    print lp.GetLen()
    print lp.GetMidPart()
    print lp.GetLongestPart()
    print lp.GetMidPoint()

    print SplitLine([10,0], [300,100], [30,30,30,30])
