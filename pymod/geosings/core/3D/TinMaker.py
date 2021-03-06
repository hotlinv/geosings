# -*- encoding: utf-8 -*-
import ogr,math
import Numeric as num
import Image,ImageDraw
from geosings.core.algorithm.vector import *
from geosings.core.algorithm.geom import *

from geosings.core.system import choose

class TINPoint:
    def __init__(self,x,y,z):
        self.x,self.y,self.z=x,y,z

def len2p(p1,p2):
    return math.sqrt(math.pow((p1.x-p2.x),2)+ \
            math.pow((p1.y-p2.y),2))

class TINEdge:
    def __init__(self,p1,p2):
        self.p1,self.p2 = p1,p2
        self.t1 = None
        self.t2 = None
    def len(self):
        return math.sqrt(math.pow((self.p1.x-self.p2.x),2)+ \
                math.pow((self.p1.y-self.p2.y),2))
    def len2(self):
        return math.pow((self.p1.x-self.p2.x),2)+ \
                math.pow((self.p1.y-self.p2.y),2)
    def iscross(self,edge2):
        """判断线段是否相交
        """
        s1 = VSegment(VP(self.p1.x,self.p1.y),VP(self.p2.x,self.p2.y))
        s2 = VSegment(VP(edge2.p1.x,edge2.p1.y),VP(edge2.p2.x,edge2.p2.y))
        return issegcross(s1,s2)

class OutSide:
    def isInCircle(self,point):
        return 0

class TINTriangle:
    def __init__(self,e1,e2,e3):
        self.e1,self.e2,self.e3 = e1,e2,e3
        self.reInit()

    def reInit(self):
        self.p1 = self.e1.p1
        self.p2 = self.e1.p2
        if self.e2.p1 != self.p1 and self.e2.p1 != self.p2:
            self.p3 = self.e2.p1
        else:
            self.p3 = self.e2.p2
        if self.e1.t1 is None: self.e1.t1 = self
        else: self.e1.t2 = self
        if self.e2.t1 is None: self.e2.t1 = self
        else: self.e2.t2 = self
        if self.e3.t1 is None: self.e3.t1 = self
        else: self.e3.t2 = self

        self.__cacCircle()
        #print 'dellr:',self.dEllR
        #print self.p1,self.p2,self.p3,self.e2.p1==self.p1
    def getPointByEdge(self, e):
        ps = [self.p1,self.p2,self.p3]
        for p in ps:
            if p != e.p1 and p != e.p2:
                return p
    def getEdgeByPoint(self, p):
        es = [self.e1,self.e2,self.e3]
        for e in es:
            if e.p1 != p and p != e.p2:
                return e

    def __cacCircle(self):
        a1,b1=self.p1.x,self.p1.y
        a2,b2=self.p2.x,self.p2.y
        a3,b3=self.p3.x,self.p3.y
        self.dEllPty=((a3-a1)*(a2*a2+b2*b2-a1*a1-b1*b1)- \
            (a2-a1)*(a3*a3+b3*b3-a1*a1-b1*b1))/(2*((a2-a1)*(b1-b3)-(b1-b2)*(a3-a1)))
        self.dEllPtx=((b1-b3)*(a1*a1+b1*b1-a2*a2-b2*b2)- \
            (b1-b2)*(a1*a1+b1*b1-a3*a3-b3*b3))/(2*((a3-a1)*(b1-b2)-(b1-b3)*(a2-a1)))
        R1=math.sqrt(math.pow(self.p1.x-self.dEllPtx,2)+pow(self.p1.y-self.dEllPty,2))
        R2=math.sqrt(math.pow(self.p2.x-self.dEllPtx,2)+pow(self.p2.y-self.dEllPty,2))
        R3=math.sqrt(math.pow(self.p3.x-self.dEllPtx,2)+pow(self.p3.y-self.dEllPty,2))
        self.dEllR=R1
        if R2<self.dEllR:self.dEllR=R2
        if R3<self.dEllR:self.dEllR=R3

    def isin(self, point):
        """判断点是否在三角形内
        """
        tmpp1 = (self.p1.x-point.x,self.p1.y-point.y)
        tmpp2 = (self.p2.x-point.x,self.p2.y-point.y)
        tmpp3 = (self.p3.x-point.x,self.p3.y-point.y)
        q1 = self.__quadrant(tmpp1)
        q2 = self.__quadrant(tmpp2)
        q3 = self.__quadrant(tmpp3)
        lines = [0,0,0,0]
        self.__isLineCross(tmpp1,tmpp2,q1,q2,lines)
        self.__isLineCross(tmpp2,tmpp3,q2,q3,lines)
        self.__isLineCross(tmpp1,tmpp3,q1,q3,lines)
        return lines[0] and lines[1] and lines[2] and lines[3]

    def isInCircle(self,point):
        """判读点是否在三角形内结园内
        """
        i=math.pow((point.x-self.dEllPtx),2)+pow((point.y-self.dEllPty),2) \
            -pow(self.dEllR,2)
        if i>0: return 0
        else: return 1


    def getAdjacentTriangles(self):
        rettas = []
        #print self.e1.t1,self.e1.t2,self
        if self.e1.t1 != self:
            rettas.append(self.e1.t1)
        elif self.e1.t2 != self:
            rettas.append(self.e1.t2)
        if self.e2.t1 != self:
            rettas.append(self.e2.t1)
        elif self.e2.t2 != self:
            rettas.append(self.e2.t2)
        if self.e3.t1 != self:
            rettas.append(self.e3.t1)
        elif self.e3.t2 != self:
            rettas.append(self.e3.t2)
        return rettas

    def __quadrant(self,p):
        if p[0]>=0 and p[1]>=0: return 1      #在一象限
        elif p[0]<0 and p[1]>=0: return 2   #在二象限
        elif p[0]<=0 and p[1]<0: return 3    #在三象限
        else: return 4    #在四象限
    def __isLineCross(self,p1,p2,q1,q2,lines):
        if q1==1 and q2==2 or q1==2 and q2==1: #在1,2象限
            lines[1]=1
        elif q1==3 and q2==4 or q1==4 and q2==3 :#在3,4象限
            lines[3]=1
        elif q1==1 and q2==4 or q1==4 and q2==1:#在1,4象限
            lines[0]=1
        elif q1==2 and q2==3 or q1==3 and q2==2:#在2,3象限
            lines[2]=1
        elif q1==1 and q2==3 or q1==3 and q2==1:#在1,3象限
            b=(p1[0]*p2[1]-p1[1]*p2[0])/(p1[0]-p2[0])
            if b>0: lines[1],lines[2]=1,1
            elif b<0: lines[0],lines[3]=1,1
            else:lines[0],lines[1],lines[2],lines[3]=1,1,1,1
        elif q1==2 and q2==4 or q1==4 and q2==2:#在2,4象限
            b=(p1[0]*p2[1]-p1[1]*p2[0])/(p1[0]-p2[0])
            if b>0: lines[0],lines[1]=1,1
            elif b<0: lines[2],lines[3]=1,1
            else:lines[0],lines[1],lines[2],lines[3]=1,1,1,1

ds = ogr.Open("line6.shp")
layer = ds.GetLayer()

#print dir(layer)
ext = layer.GetExtent()#x,x,y,y
print ext

INITH = 100

points = [TINPoint(ext[0]-10,ext[3]+10,INITH), \
        TINPoint(ext[1]+10,ext[3]+10,INITH), \
        TINPoint(ext[1]+10,ext[2]-10,INITH), \
        TINPoint(ext[0]-10,ext[2]-10,INITH)]

pids = [id(p) for p in points]
edges = [TINEdge(points[0],points[1]),TINEdge(points[1],points[3]),
        TINEdge(points[3],points[0]),TINEdge(points[1],points[2]),
        TINEdge(points[2],points[3])]
for ei in range(len(edges)):
    if ei!=1:
        edges[ei].t1 = OutSide()#设置最外面的拓扑
eids = [id(e) for e in edges]
tris = [TINTriangle(edges[0],edges[1],edges[2]),
        TINTriangle(edges[3],edges[4],edges[1])]
tids = [id(t) for t in tris]

def delPoint(p):
    i = pids.index(id(p))
    points.pop(i)
    pids.pop(i)
def addPoint(p):
    points.append(p)
    pids.append(id(p))
def delEdge(e):
    i = eids.index(id(e))
    edges.pop(i)
    eids.pop(i)
def delEdgeById(eid):
    #print eid,eids
    i = eids.index(eid)
    edges.pop(i)
    eids.pop(i)
    #print eids
def addEdge(e):
    edges.append(e)
    eids.append(id(e))
def delTriangle(t):
    i = tids.index(id(t))
    tris.pop(i)
    tids.pop(i)
def delTriangleById(tid):
    i = tids.index(tid)
    tris.pop(i)
    tids.pop(i)
def addTriangle(t):
    tris.append(t)
    tids.append(id(t))

leftedges = []
rmedges = []
deltris = [] #要删除的三角形
#tp1,tp2,tp3 = TINPoint(0,0,0),TINPoint(3,0,0),TINPoint(3,4.0,0)
#te1,te2,te3 = TINEdge(tp1,tp2),TINEdge(tp2,tp3),TINEdge(tp3,tp1)
#ttest=TINTriangle(te1,te2,te3)
#print ttest.dEllR

#print [edges[i].len() for i in range(len(edges))]

def findAffectTa(ta,p):
    deltris.append(id(ta))
    e1i = id(ta.e1)
    e2i = id(ta.e2)
    e3i = id(ta.e3)
    if e1i in leftedges:
        leftedges.remove(e1i)
        rmedges.append(e1i)
    else:
        leftedges.append(e1i)

    if e2i in leftedges:
        leftedges.remove(e2i)
        rmedges.append(e2i)
    else:
        leftedges.append(e2i)

    if e3i in leftedges:
        leftedges.remove(e3i)
        rmedges.append(e3i)
    else:
        leftedges.append(e3i)

    #print "*"*10
    tris = ta.getAdjacentTriangles()
    for t in tris:
        if t.__class__==OutSide:
            continue
        if (t is not None) and not (id(t) in deltris) and (t.isInCircle(p)):
            #print t,"*"*10,deltris,t in deltris
            findAffectTa(t,p)

def CheakPointsInSameLine(edge,p):
    if (edge.p2.x-edge.p1.x)*(edge.p1.y-p.y)-(edge.p1.y-edge.p2.y)*(p.x-edge.p1.x)==0:
        return 1
    else:return 0
    
def deleteTriangles():
    for eid in leftedges:
        e = edges[eids.index(eid)]
        if id(e.t1) in deltris:
            e.t1 = None
        if id(e.t2) in deltris:
            e.t2 = None
    delEdgs()
    delTris()

def delEdgs():
    #print rmedges
    for e in rmedges:
        delEdgeById(e)

def delTris():
    for ta in deltris:
        delTriangleById(ta)

def sortEdges():
    if len(leftedges)<3:
        print "sort edges error1"
        return
    tmpes = [edges[eids.index(eid)] for eid in leftedges] 
    for ei in range(len(leftedges)-1):
        e1 = tmpes[ei]
        for ei2 in range(ei+1,len(leftedges)):
            e2 = tmpes[ei2]
            if e2.p1==e1.p2 or e2.p2==e1.p2:
                #print e1.p2,e2.p1,e2.p2
                if ei2!=ei+1:
                    tmpe=leftedges[ei+1];leftedges[ei+1]=leftedges[ei2];leftedges[ei2]=tmpe
                    tmpe=tmpes[ei+1];tmpes[ei+1]=tmpes[ei2];tmpes[ei2]=tmpe

                if e1.p2 == e2.p1:
                    pass
                elif e1.p2 == e2.p2:
                    tmpp=e2.p2;e2.p2=e2.p1;e2.p1=tmpp
                else:
                    print "sort edges error3","x"*200
                    return 
                break
    #print leftedges,"*"*10

def addTriangles(p):
    firste = None
    laste = None
    for ei in range(len(leftedges)):
        e2 = edges[eids.index(leftedges[ei])]
        if ei==0:
            e1 = TINEdge(p,e2.p1)
            firste = e1
            addEdge(e1)
        else:
            e1 = laste
        if ei!=len(leftedges)-1:
            e3 = TINEdge(e2.p2,p)
            laste = e3
            addEdge(e3)
        else:
            e3 = firste
        tri = TINTriangle(e1,e2,e3)
        addTriangle(tri)
    firste.t2 = tris[-1]

#findAffectTa(tris[0], points[0])
#print tris[0].getAdjacentTriangles()
    
#print tris,edges

def delNoNeed():
    global deltris
    deltris = []
    for ta in tris:
        if ta.p1.z==INITH or ta.p2.z==INITH or \
             ta.p3.z==INITH:
            deltris.append(id(ta))
    for ta in deltris:
        delTriangleById(ta)

def draw():
    minx = min(ext[0],ext[1]-20)
    miny = min(ext[2],ext[3]-20)
    width = math.fabs(ext[0]-ext[1])+40
    height = math.fabs(ext[2]-ext[3])+40

    w = 1000
    h = height/width*w
    scale = 1000.0/width
    im = Image.new("L",(int(w),int(h)),255)
    draw = ImageDraw.Draw(im)

    for t in tris:
        draw.polygon((((t.p1.x-minx)*scale,(t.p1.y-miny)*scale),
            ((t.p2.x-minx)*scale,(t.p2.y-miny)*scale),
            ((t.p3.x-minx)*scale,(t.p3.y-miny)*scale)) ,fill=120, outline=0)

    del draw

    im.save("output.png", "PNG")

def output(oname):
    prj = '''PROJCS["Beijing 1954 / Gauss-Kruger zone 17",GEOGCS["Beijing
    1954",DATUM["Beijing_1954",SPHEROID["Krassowsky
    1940",6378245,298.3,AUTHORITY["EPSG","7024"]],AUTHORITY["EPSG","6214"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4214"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",99],PARAMETER["scale_factor",1],PARAMETER["false_easting",17500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","21417"]]'''

    import struct
    f = open(oname,"w")
    data = struct.pack('5siiii',"tin01",len(points),len(tris),5+4*4+len(prj),len(prj))

    f.write(data)
    f.write(prj)
    for p in points:
        pdatas = struct.pack("ddf",p.x,p.y,float(p.z))
        f.write(pdatas)
    for t in tris:
        pdatas = struct.pack("iii",pids.index(id(t.p1))+1,
                pids.index(id(t.p2))+1,
                pids.index(id(t.p3))+1)
        f.write(pdatas)
    f.close()

def output_model(facearray,pointarray,filename):
    from Dice3DS import dom3ds
    import numpy

    n = len(pointarray)
    m = len(facearray)

    padfacearray = numpy.zeros((n,4),numpy.uint32)
    padfacearray[:,:3] = facearray
    padfacearray[:,3] = 7

    smoothing = numpy.ones(m,numpy.uint32)

    obj = dom3ds.N_TRI_OBJECT()
    obj.points = dom3ds.POINT_ARRAY(npoints=n,array=pointarray)
    obj.faces = dom3ds.FACE_ARRAY(nfaces=m,array=padfacearray)
    obj.faces.smoothing = dom3ds.SMOOTH_GROUP(array=smoothing)
    obj.matrix = dom3ds.MESH_MATRIX(array=numpy.identity(4,numpy.float32))
    
    nobj = dom3ds.NAMED_OBJECT(name="OBJECT",obj=obj)

    dom = dom3ds.M3DMAGIC()
    dom.version = dom3ds.M3D_VERSION(number=3)
    dom.mdata = dom3ds.MDATA()
    dom.mdata.scale = dom3ds.MASTER_SCALE(value=1.0)
    dom.mdata.objects = [ nobj ]
    
    dom3ds.write_3ds_file(filename,dom)

maxz = 0
minz = 10000
def output3ds(oname):
    import numpy,math
    global maxz,minz
    minx = min(ext[0],ext[1]-20)
    miny = min(ext[2],ext[3]-20)
    midx = (ext[0]+ext[1])/2.0
    midy = (ext[2]+ext[3])/2.0
    width = math.fabs(ext[0]-ext[1])+40
    height = math.fabs(ext[2]-ext[3])+40

    w = 30.0
    h = height/width*w
    scale = 30.0/width

    pdatas = []
    for p in points:
        pdatas.append([(p.x-midx)*scale,(p.y-midy)*scale, \
            50.0*((p.z-minz)/(maxz))])
    
    tdatas = []
    for t in tris:
        tdatas.append([pids.index(id(t.p1)),
                pids.index(id(t.p2)),
                pids.index(id(t.p3))])
    pointarr = numpy.array(pdatas)
    facearr = numpy.array(tdatas)

    if len(pointarr)>len(facearr):
        extarray = numpy.zeros((len(pointarr)-len(facearr),3),numpy.uint32)
        facearr=numpy.concatenate([facearr,extarray])
    if len(pointarr)<len(facearr):
        extarray = numpy.zeros((len(facearr)-len(pointarr),3),numpy.float)
        pointarr=numpy.concatenate([pointarr,extarray])

    print facearr.shape,pointarr.shape
    print maxz,minz,"^"*10,pointarr[0]
    output_model(facearr,pointarr,oname)

def isCrackTa(ta):
    """判断是否是破碎边缘三角形
    """
    if ta.p1.z==ta.p2.z==ta.p3.z or \
        ta.p1.z!=ta.p2.z!=ta.p3.z!=ta.p1.z:#三点都在同一高度或者都不在同一高度
        return None
    same_e = None
    if ta.e1.p1.z == ta.e1.p2.z:
        same_e = ta.e1
    elif ta.e2.p1.z == ta.e2.p2.z:
        same_e = ta.e2
    elif ta.e3.p1.z == ta.e3.p2.z:
        same_e = ta.e3
    else: return None
    ta2 = choose(same_e.t1==ta,same_e.t2,same_e.t1)
    if ta2.__class__==OutSide:
        return None
    if ta2.p1.z!=ta2.p2.z!=ta2.p3.z:#另一个三角形三点不在一个平面，就不是
        return None
    p1 = ta.getPointByEdge(same_e)
    p2 = ta2.getPointByEdge(same_e)
    ta2ps = [ta2.p1,ta2.p2,ta2.p3]
    ta2ps = [e for e in ta2ps if e!=p2]
    #print ta2lines
    if getCos(p2,ta2ps[0],ta2ps[1])>=0:
        return None#如果角度小于90，则不是
    #看是否可以交换线段（两条线段是否相交）
    if same_e.iscross(TINEdge(p1,p2)):
        return ta,ta2,same_e,p1,p2
    else:
        return None
def MakeCrackTaRight(ta1,ta2,comedge,p1,p2):
    """ 交互对角线
    """
    enocom = []
    es1 = [ta1.e1,ta1.e2,ta1.e3]
    for e in es1:
        if e != comedge:
            enocom.append(e)
            if e.t1==ta1:
                e.t1 = None
            elif e.t2==ta1:
                e.t2 = None
    es2 = [ta2.e1,ta2.e2,ta2.e3]
    for e in es2:
        if e != comedge:
            enocom.append(e)
            if e.t1==ta2:
                e.t1 = None
            elif e.t2==ta2:
                e.t2 = None
    taearr1 = []
    taearr2 = []
    for e in enocom:
        if e.p1==comedge.p1 or e.p2==comedge.p1:
            taearr1.append(e)
        else:
            taearr2.append(e)

    comedge.p1 = p1
    comedge.p2 = p2
    ta1.e1,ta1.e2,ta1.e3 = taearr1[0],taearr1[1],comedge
    ta2.e1,ta2.e2,ta2.e3 = taearr2[0],taearr2[1],comedge

    ta1.reInit()
    ta2.reInit()

def ImproveCrackTa():
    """修改破碎边缘三角形
    """
    i = 0
    while(i<len(tris)):
        ta = tris[i]
        ret = isCrackTa(ta)
        if ret is not None:
            ta1,ta2,com_e,p1,p2=ret
            MakeCrackTaRight(ta1,ta2,com_e,p1,p2)
            print '\r',i,len(tris),
            i=0
        else:
            i+=1

def willBeChange(ta):
    if ta is not None and ta.__class__!=OutSide \
        and ta.p1.z==ta.p2.z==ta.p3.z:
        zz = ta.p1.z
        z = [-50000]*9
        ntas = ta.getAdjacentTriangles()
        if ntas[0] is not None and ntas[0].__class__!=OutSide:
            z[0] = ntas[0].p1.z
            z[1] = ntas[0].p2.z
            z[2] = ntas[0].p3.z
        if ntas[1] is not None and ntas[1].__class__!=OutSide:
            z[3] = ntas[1].p1.z
            z[4] = ntas[1].p2.z
            z[5] = ntas[1].p3.z
        if ntas[2] is not None and ntas[2].__class__!=OutSide:
            z[6] = ntas[2].p1.z
            z[7] = ntas[2].p2.z
            z[8] = ntas[2].p3.z
        a=[]
        for i in z:
            if i!=zz and i!=-50000:
                a.append(i)
        if len(a)==2 :#and a[0]!=a[1]:
            return 1
        else: return 0
   
def isTa3pSameElev(ta):
    if ta is not None and ta.__class__!=OutSide \
            and ta.p1.z==ta.p2.z==ta.p3.z==ta.p1.z:
        return 1
    else:
        return 0
def findRightTa(tas,nowtaorder):
    """查找连成片的拓展三角形
    """
    nowta = None
    if nowtaorder:
        nowta = tas[len(tas)-1]
    else:
        nowta = tas[0]
    ntas = nowta.getAdjacentTriangles()
    #if len(ntas)==1:
    #    ntas.append(None)
    #    ntas.append(None)
    #if len(ntas)==2:
    #    ntas.append(None)
    if ntas[0] in tas:
        ntas[0]=None
    if ntas[1] in tas:
        ntas[1]=None
    if ntas[2] in tas:
        ntas[2]=None
    is1same = isTa3pSameElev(ntas[0])
    is2same = isTa3pSameElev(ntas[1])
    is3same = isTa3pSameElev(ntas[2])
    #print nowta.p1.z,nowta.p2.z,ntas[0].p3.z
    #if ntas[0] is not None and ntas[0].__class__!=OutSide:
    #    print is1same,ntas[0].p1.z,ntas[0].p2.z,ntas[0].p3.z
    #if ntas[1] is not None and ntas[1].__class__!=OutSide:
    #    print is2same,ntas[1].p1.z,ntas[1].p2.z,ntas[1].p3.z
    #if ntas[2] is not None and ntas[2].__class__!=OutSide:
    #    print is3same,ntas[2].p1.z,ntas[2].p2.z,ntas[2].p3.z
    rta = None
    if is1same and is2same and is3same:
        maxl = nowta.e1.len();rta = ntas[0]
        if nowta.e2.len()>maxl:
            maxl = nowta.e2.len();rta = ntas[1]
        if nowta.e3.len()>maxl:
            maxl = nowta.e3.len();rta = ntas[2]
    elif is1same and is2same:#两个都是三点在同一个高度
        if nowta.e1.len()>nowta.e2.len():
            rta=ntas[0]
        else: rta=ntas[1]
    elif is1same and is3same:#两个都是三点在同一个高度
        if nowta.e1.len()>nowta.e3.len():
            rta=ntas[0]
        else: rta=ntas[2]
    elif is2same and is3same:#两个都是三点在同一个高度
        if nowta.e2.len()>nowta.e3.len():
            rta=ntas[1]
        else: rta=ntas[2]
    elif is1same:
        rta = ntas[0]
    elif is2same:
        rta = ntas[1] 
    elif is3same:
        rta = ntas[2]
    else:
        rta = None
    return rta

turnUpOrDown1 = 0
turnUpOrDown2 = 0

def findElevRange(taarr):
    global turnUpOrDown1
    global turnUpOrDown2
    turnUpOrDown1 = 0
    turnUpOrDown2 = 0
    tao1,tao2 = taarr[0],taarr[len(taarr)-1]
    elev = tao1.p1.z
    tans1 = tao1.getAdjacentTriangles()
    tans2 = tao2.getAdjacentTriangles()
    #找出不在同一高度的的三角形
    sel_pe = []
    for ta in tans1:
        if not isTa3pSameElev(ta):
            if ta.p1.z != elev:
                sel_pe.append([ta.p1,ta.getEdgeByPoint(ta.p1)])
            if ta.p2.z != elev:
                sel_pe.append([ta.p2,ta.getEdgeByPoint(ta.p2)])
            if ta.p3.z != elev:
                sel_pe.append([ta.p3,ta.getEdgeByPoint(ta.p3)])
    print sel_pe[0][0].z,sel_pe[1][0].z,elev,"#"*10
    lager1 = sel_pe[0][0].z>elev and sel_pe[1][0].z>elev
    lager2 = sel_pe[0][0].z<elev and sel_pe[1][0].z<elev
    print lager1,lager2
    if lager1 or lager2:#要提到和elev一个档次
        tp1,tp2 = id(sel_pe[0][1].p1),id(sel_pe[0][1].p2)
        tp3,tp4 = id(sel_pe[1][1].p1),id(sel_pe[1][1].p2)
        p1 = choose((tp1==tp3 or tp1==tp4), sel_pe[0][1].p1, sel_pe[0][1].p2)
        if lager1:
            turnUpOrDown1 = max(elev-sel_pe[0][0].z, \
                    elev-sel_pe[1][0].z) #下坡
        else:
            turnUpOrDown1 = min(elev-sel_pe[0][0].z, \
                    elev-sel_pe[1][0].z) #上坡
    else:
        if sel_pe[0][1].len()>sel_pe[1][1].len():
            p1 = sel_pe[0][0]
        else:
            p1 = sel_pe[1][0]
    sel_pe = []
    for ta in tans2:
        if not isTa3pSameElev(ta):
            if ta.p1.z != elev:
                sel_pe.append([ta.p1,ta.getEdgeByPoint(ta.p1)])
            if ta.p2.z != elev:
                sel_pe.append([ta.p2,ta.getEdgeByPoint(ta.p2)])
            if ta.p3.z != elev:
                sel_pe.append([ta.p3,ta.getEdgeByPoint(ta.p3)])
    print sel_pe[0][0].z,sel_pe[1][0].z,"#"*10
    lager1 = sel_pe[0][0].z>elev and sel_pe[1][0].z>elev
    lager2 = sel_pe[0][0].z<elev and sel_pe[1][0].z<elev
    if lager1 or lager2:#要提到和elev一个档次
        tp1,tp2 = id(sel_pe[0][1].p1),id(sel_pe[0][1].p2)
        tp3,tp4 = id(sel_pe[1][1].p1),id(sel_pe[1][1].p2)
        p2 = choose((tp1==tp3 or tp1==tp4), sel_pe[0][1].p1, sel_pe[0][1].p2)
        if lager1:
            turnUpOrDown2 = max(elev-sel_pe[0][0].z, \
                    elev-sel_pe[1][0].z) #下坡
        else:
            turnUpOrDown2 = min(elev-sel_pe[0][0].z, \
                    elev-sel_pe[1][0].z) #上坡
    else:
        if sel_pe[0][1].len()>sel_pe[1][1].len():
            p2 = sel_pe[0][0]
        else:
            p2 = sel_pe[1][0]
    return p1,p2

insertps = []
def InsertToCenter(taa,hi,ei):
    """找到两头的三角形依次内插中心点
    """
    global insertps
    tahi = taa[hi]
    x1,y1 = tahi.p1.x,tahi.p1.y
    x2,y2 = tahi.p2.x,tahi.p2.y
    x3,y3 = tahi.p3.x,tahi.p3.y
    x12,y12 = (x1+x2)/2.0,(y1+y2)/2.0
    newp = TINPoint((x12+x3)/2.0,(y12+y3)/2.0,100)
    insertps.append(newp)
    while taa[hi].isInCircle(newp) and hi!=ei or \
            taa[hi].isin(newp) and hi!=ei:
        if hi<ei : hi+=1
        else: hi-=1
    if hi==ei:
        tahi = taa[hi]
        x1,y1 = tahi.p1.x,tahi.p1.y
        x2,y2 = tahi.p2.x,tahi.p2.y
        x3,y3 = tahi.p3.x,tahi.p3.y
        x12,y12 = (x1+x2)/2.0,(y1+y2)/2.0
        newp = TINPoint((x12+x3)/2.0,(y12+y3)/2.0,100)
        insertps.append(newp)
    else:
        InsertToCenter(taa,ei,hi)

def WriteRightElev(p1, p2, taa):
    """给内插的点付正确的高程值
    """
    global turnUpOrDown1
    global turnUpOrDown2
    elevthis = taa[0].p1.z#等高高程
    totlelong1=len2p(p1,insertps[0])
    totlelong2=len2p(p2,insertps[1])
    for i in range(0,len(insertps)-2,2):
        totlelong1+=len2p(insertps[i],insertps[i+2])
    for i in range(1,len(insertps)-2,2):
        totlelong2+=len2p(insertps[i],insertps[i+2])
    if p1.z!=p2.z:
        elevmid=choose(p1.z>p2.z,p2.z+(totlelong2/(totlelong1+totlelong2)*(p1.z-p2.z)), \
                p1.z+(totlelong1/(totlelong1+totlelong2)*(p2.z-p1.z)))
    else:
        if turnUpOrDown1*turnUpOrDown1>0:
            elevmid = elevthis+(turnUpOrDown1+turnUpOrDown2)/2.0/2.0
        else:
            elevmid = elevthis
    print "mid:",elevmid, "elev this",elevthis,"point count:",len(insertps)
    #mp = insertps[len(insertps)-1]
    #mp.z = elevmid
    nowlong1=len2p(p1,insertps[0])
    for ip in range(0,len(insertps),2):
        if ip==0:
            nowlong1=len2p(p1,insertps[0])
        else:
            nowlong1+=len2p(insertps[ip-2],insertps[ip])
        mp = insertps[ip]
        mp.z = p1.z+(nowlong1/totlelong1*(elevmid-p1.z))
        print '\n',"0000000000000",mp.z,ip,mp.x,mp.y
    nowlong2=len2p(p2,insertps[1])
    for ip in range(1,len(insertps),2):
        if ip==1:
            nowlong2=len2p(p2,insertps[1])
        else:
            nowlong2+=len2p(insertps[ip-2],insertps[ip])
        mp = insertps[ip]
        mp.z = p2.z+(nowlong2/totlelong2*(elevmid-p2.z))
        print '\n',"11111111111",mp.z,ip,mp.x,mp.y

noNeedtaIds = []

def InsertPoints():
    global insertps,isINeedta,noNeedtaIds
    flag = 1
    while flag:
        isINeedta = []
        insertps = []
        for ta in tris:
            if willBeChange(ta) and id(ta) not in noNeedtaIds:
                isINeedta.append(ta)
                break
        if len(isINeedta):
            while 1:#向两边扩展
                ta = findRightTa(isINeedta,1)
                if ta is not None and ta.__class__!=OutSide:
                    isINeedta.append(ta)
                else: break
            while 1:#向两边扩展
                ta = findRightTa(isINeedta,0)
                if ta is not None and ta.__class__!=OutSide:
                    isINeedta.insert(0,ta)
                else: break
            ep1,ep2 = findElevRange(isINeedta)
            print ep1.z,ep2.z
            InsertToCenter(isINeedta,0,len(isINeedta)-1);
            WriteRightElev(ep1,ep2,isINeedta)
            if not len(insertps):
                noNeedtaIds.extend([id(t) for t in isINeedta])
            #for t in isINeedta:
            #    delTriangle(t)
                
            for p in insertps:
                if not insertPoint(p):
                    pass
            #ImproveCrackTa()
            print len(isINeedta),len(insertps)
        else:
            break
        #flag = 0
    print len(noNeedtaIds)

def insertPoint(p):
    global deltris,leftedges,rmedges
    global eids,pids,tids
    global points,tris,edges
    global maxz,minz
    deltris = []
    leftedges = []
    rmedges = []
    if p.z>maxz: maxz=p.z
    if p.z<minz: minz=p.z
    for ti in range(len(tris)-1,-1,-1):
        #print t.p1.x,t.p1.y,t.p2.x,t.p2.y,t.p3.x,t.p3.y,"*"*10,p.x,p.y
        t = tris[ti]
        if t.isin(p):
            findAffectTa(t,p)
            #print "#"*10,t,p.x,p.y
            break
    isfine = 1
    for eid in leftedges:
        e = edges[eids.index(eid)]
        if CheakPointsInSameLine(e,p):
            isfine = 0
            break
    if not isfine:
        return
    sortEdges()
    #for t in deltris:
    #    destroy(t)
    #print "left edges:",leftedges
    deleteTriangles()
    addTriangles(p)

    addPoint(p)
    return 1
def main():
    fcount = layer.GetFeatureCount()
    feature = layer.GetNextFeature()
    c = 0
    while feature :
        g = feature.GetGeometryRef()
        gc = g.GetGeometryCount()
        if gc==0:
            geom=g
            pointcount = geom.GetPointCount()
            for i in range(pointcount):
                p=TINPoint(geom.GetX(i),geom.GetY(i),float(feature.GetField("ELEV")))
                insertPoint(p)
                print "\r",i,"/",geom.GetPointCount(),"(",c,":",fcount,")"," "*30,
        else:
            for gi in range(gc):
                geom=g.GetGeometryRef(gi)
                pointcount = geom.GetPointCount()
                for i in range(pointcount):
                    p=TINPoint(geom.GetX(i),geom.GetY(i),float(feature.GetField("ELEV")))
                    insertPoint(p)
                    print "\r",i,"/",geom.GetPointCount(),"(",c,":",fcount,")"," "*30,
        #print "\r",c,"/",fcount,
        feature = layer.GetNextFeature()
        c+=1
    print 
    ImproveCrackTa()
    print
    InsertPoints()
    delNoNeed()
    print "draw lines..."
    draw()
    print "output 3d module..."
    output3ds("aa.3ds")

main()

import profile
#profile.run("main()", "prof.plog")
profile.run("", "prof.plog")
import sys
import pstats

if len(sys.argv)>1:
    pyname = sys.argv[1]+".py"
else:
    pyname = ""
p = pstats.Stats("prof.plog")
#"LayerCanvas.py"
p.strip_dirs().sort_stats("time").print_stats("TinMaker")


