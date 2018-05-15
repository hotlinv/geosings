# -*- encoding: utf-8 -*-
"""
定义几何运算和几何判断

 - linux_23;2007.9.29;创建
"""
from vector import *
import math

def issegcross(s1,s2):
    """判断线段是否相交
    """
    p1=s1.pf
    p2=s1.pt
    q1=s2.pf
    q2=s2.pt
    p1q1 = VSegment(p1,q1)
    q2q1 = VSegment(q2,q1)
    p2q1 = VSegment(p2,q1)
    q1p1 = VSegment(q1,p1)
    p2p1 = VSegment(p2,p1)
    q2p1 = VSegment(q2,p1)
    return max(s1.pf.x,s1.pt.x)>=min(s2.pf.x,s2.pt.x) and \
          max(s2.pf.x,s2.pt.x)>=min(s1.pf.x,s1.pt.x) and \
          max(s1.pf.y,s1.pt.y)>=min(s2.pf.y,s2.pt.y) and \
          max(s2.pf.y,s2.pt.y)>=min(s1.pf.y,s1.pt.y) and \
          p1q1.xmultiply(q2q1.v)*q2q1.xmultiply(p2q1.v)>=0 and \
          q1p1.xmultiply(p2p1.v)*p2p1.xmultiply(q2p1.v)>=0
   
#def checkAngle(s1,s2):
#    return s1.pmultiply(s2.v)

def getlen(p1,p2):
    l = math.sqrt(math.pow((p1.x-p2.x),2)+ \
            math.pow((p1.y-p2.y),2))
    return l

def getCos(p1,p2,p3):
    """
    """
    a = getlen(p2,p3)
    b = getlen(p1,p2)
    c = getlen(p1,p3)
    return (b*b+c*c-a*a)/2*b*c  

if __name__=="__main__":
    s1 = VSegment(VP(0,0),VP(1,0))
    s2 = VSegment(VP(0.5,-1),VP(0.5,1))
    print issegcross(s1,s2)

    s1 = VSegment(VP(0,0),VP(1,0))
    s2 = VSegment(VP(0.5,1),VP(0.5,2))
    print issegcross(s1,s2)
    
    s1 = VSegment(VP(0,0),VP(1,1))
    s2 = VSegment(VP(0,1),VP(1,0))
    print issegcross(s1,s2)

    s1 = VSegment(VP(1,1),VP(0,0))
    s2 = VSegment(VP(0,1),VP(1,0))
    print issegcross(s1,s2)

    s1 = VSegment(VP(0,0),VP(0.4,0.4))
    s2 = VSegment(VP(0,1),VP(1,0))
    print issegcross(s1,s2)

    s1 = VSegment(VP(0,0),VP(0.5,0.5))
    s2 = VSegment(VP(0,1),VP(1,0))
    print issegcross(s1,s2)

    #s1 = VSegment(VP(0,0),VP(1,0))
    #s2 = VSegment(VP(-1,1),VP(0,0))
    #print checkAngle(s1,s2)

    print getCos(VP(0,0),VP(3,0),VP(0,4))
