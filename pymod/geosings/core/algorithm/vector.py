# -*- encoding: utf-8 -*-
"""
定义矢量运算

 - linux_23;2007.9.29;创建
"""
class VP:
    def __init__(self, x,y):
        self.x = x
        self.y = y

def vxmultiply(p1,p2):
    """向量叉乘
    """
    return p1.x*p2.y-p2.x*p1.y

#def vpmultiply(p1,p2):
#    """向量点乘
#    """
#    return p1.x*p2.x+p1.y*p2.y
    
def vsub(p1,p2):
    """向量相减
    """
    return VP(p1.x-p2.x,p1.y-p2.y)


class VSegment:
    """向量线段
    """
    def __init__(self,p1,p2):
        self.pf = p1
        self.pt = p2
        self.v = vsub(p1,p2)

    def xmultiply(self,v):
        return vxmultiply(self.v, v)

    #def pmultiply(self,v):
    #    return vpmultiply(self.v, v)
