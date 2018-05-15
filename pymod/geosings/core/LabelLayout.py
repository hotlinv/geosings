# -*- coding: utf-8 -*-
"""
该模块进行Symbol的摆放算法的思想

 - writer:linux_23; create:2007.5.31 ; version:1; 创建
"""
import Numeric as nu
from geosings.core.system import cz_split
from geosings.core.Geom import SplitLine,CreatePolygon
import Image,ImageDraw,math,ogr


def getmaxareageom(geom):
    if type(geom)==list:
        count = len(geom)
        which = 0
        maxarea = 0
        rg = None
        for i in range(count):
            tg = getmaxareageom(geom[i])
            if tg is not None :
                #print g.GetGeometryCount()
                area = tg.GetArea()
            else: area = 0
            #print area
            if area>maxarea:
                maxarea = area
                which =i
                rg = tg
        #print "!!!!!",maxarea
        return rg
    else:
        count = geom.GetGeometryCount()
        tp = geom.GetGeometryType()
        if tp == ogr.wkbPolygon:
            return geom
        if count ==0:
            return None
        which = 0
        maxarea = 0
        for i in range(count):
            area = geom.GetGeometryRef(i).GetArea()
            print area
            if area>maxarea:
                maxarea = area
                which=i
        return geom.GetGeometryRef(which)
        
def GetBetterCentroid(geom, fontsize = None):
    """获取几何形状的更好的重心（对凹多边形，争取在几何形状中）
    """
    p = geom.Centroid()
    cp = int(p.GetX()),int(p.GetY())
    e = geom.GetEnvelope()
    width = max(e[0],e[1])
    height = max(e[2],e[3])
    im = Image.new('L',(width,height),10)
    #print cp,width,height
    draw = ImageDraw.Draw(im)
    #xys = arr.tolist()
    ring = geom.GetGeometryRef(0)
    xys = [(ring.GetX(i),ring.GetY(i)) for i in range(ring.GetPointCount())]
    #print xys
    draw.polygon(xys,fill=0)
    rp = p
    #下面是一定要处理的情况（中心点直接在多边形外）
    if cp[0]>width or cp[0]<0 or cp[1]>height or cp[1]<0 or im.getpixel(cp)!=0:
        rect1 = [[0,cp[1]-1],[width,cp[1]-1],
                [width,cp[1]+1],[0,cp[1]+1]]
        gr1 = CreatePolygon(nu.array(rect1))
        gr1.CloseRings()
        rect2 = [[cp[0]-1,0],[cp[0]+1,0],
                [cp[0]+1,height],[cp[0]-1,height]]
        gr2 = CreatePolygon(nu.array(rect2))
        gr2.CloseRings()
        interg1 = gr1.Intersection(geom)
        if interg1.GetGeometryCount()>1:
            g1 = getmaxareageom(interg1)
        else:
            g1 = interg1
        interg2 = gr2.Intersection(geom)
        if interg2.GetGeometryCount()>1:
            g2 = getmaxareageom(interg2)
        else:
            g2 = interg2
        #print g1,g2
        if g1.GetArea()>g2.GetArea():
            rp = g1.Centroid()
        else:
            rp = g2.Centroid()
    #字体范围在多边形外
    if fontsize is not None:
        s = sum(im.crop((int(cp[0]-fontsize[0]/2),int(cp[1]-fontsize[1]/2), \
                int(cp[0]+fontsize[0]/2),int(cp[1]+fontsize[1]/2))).getdata())
        if s!=0:
            rectl = [[0,cp[1]-fontsize[1]/2],[cp[0],cp[1]-fontsize[1]/2],
                    [cp[0],cp[1]+fontsize[1]/2],[0,cp[1]+fontsize[1]/2]]
            gr1 = CreatePolygon(nu.array(rectl))
            gr1.CloseRings()
            interg1 = geom.Intersection(gr1)

            rectt = [[cp[0]-fontsize[0]/2,0],[cp[0]+fontsize[0]/2,0],
                    [cp[0]+fontsize[0]/2,cp[1]],[cp[0]-fontsize[0]/2,cp[1]]]
            gr2 = CreatePolygon(nu.array(rectt))
            gr2.CloseRings()
            interg2 = geom.Intersection(gr2)

            rectr = [[cp[0],cp[1]-fontsize[1]/2],[width,cp[1]-fontsize[1]/2],
                    [width,cp[1]+fontsize[1]/2],[cp[0],cp[1]+fontsize[1]/2]]
            gr3 = CreatePolygon(nu.array(rectr))
            gr3.CloseRings()
            interg3 = geom.Intersection(gr3)

            rectb = [[cp[0]-fontsize[0]/2,cp[1]],[cp[0]+fontsize[0]/2,height],
                    [cp[0]+fontsize[0]/2,height],[cp[0]-fontsize[0]/2,cp[1]]]
            gr4 = CreatePolygon(nu.array(rectb))
            gr4.CloseRings()
            interg4 = geom.Intersection(gr4)


            maxg = getmaxareageom([interg1,interg2,interg3,interg4])
            try:
                #print maxg
                if maxg is not None:
                    
                    cid = maxg.Centroid()

                    rf = [[cp[0]-fontsize[0]/2,cp[1]-fontsize[1]/2],[cp[0]+fontsize[0]/2,cp[1]-fontsize[1]/2],
                            [cp[0]+fontsize[0]/2,cp[1]+fontsize[1]/2],[cp[0]-fontsize[0]/2,cp[1]+fontsize[1]/2]]
                    rf1 = CreatePolygon(nu.array(rf))
                    rf1.CloseRings()
                    rinterg1 = geom.Intersection(rf1)

                    ccp = int(cid.GetX()),int(cid.GetY())
                    rcf = [[ccp[0]-fontsize[0]/2,ccp[1]-fontsize[1]/2],[ccp[0]+fontsize[0]/2,ccp[1]-fontsize[1]/2],
                            [ccp[0]+fontsize[0]/2,ccp[1]+fontsize[1]/2],[ccp[0]-fontsize[0]/2,ccp[1]+fontsize[1]/2]]
                    rf2 = CreatePolygon(nu.array(rcf))
                    rf2.CloseRings()
                    rinterg2 = geom.Intersection(rf2)

                    if rinterg1.GetArea()<rinterg2.GetArea():
                        print "oooooooo",cid,p
                        return cid
            except :
                print "oh no!!!!!!!!!!!!!", maxg
                pass
    return rp

class LabelLayout:
    """Symbol排列算法类
    """
    def __init__(self,symbols,dcrect):
        """初始化
        symbols的结构是一个字典。包括
        font: 字体大小（用来算标签大小）
        points: 点集合。
        off: 标记离点的距离
        lines: 线集合。(还没有实现)
        texts: 要标注的字集合
        """
        self.__syms = symbols
        self.__dcrect = dcrect
        self.w = dcrect.GetWidth()
        self.h = dcrect.GetHeight()
        self.__canv = nu.zeros((self.h,self.w))
        self.__mask = nu.arange(self.w*self.h)
        self.__mask.shape = self.__canv.shape
        self.__dc = self.__syms["dc"]
        self.__fontclass = self.__syms["fontclass"]
        #self.__fontu = self.__fontclass(self.__font,self.__dc)
        self.__off = self.__syms["off"]
        self.__dcl = dcrect.GetLeft()
        self.__dcr = dcrect.GetRight()
        self.__dct = dcrect.GetTop()
        self.__dcb = dcrect.GetBottom()

    def Layout(self,_dc=None):
        """为外部调用以排列Symbol
        dc为内部测试使用，不建议外部使用
        """
        ps = self.__syms["points"]
        ls = self.__syms["lines"]
        pls = self.__syms["polygons"]
        return self.__LayoutP(ps,_dc)+self.__LayoutL(ls,_dc)+ \
                self.__LayoutPL(pls,_dc)

    def _output(self):
        import Image,ImageDraw
        im = Image.new("L",(self.w,self.h),0)
        draw = ImageDraw.Draw(im)
        ps = self.__syms["points"]
        self.Layout(draw)
        for p in ps:
            for i in p[1]:
                draw.point(i[0],fill=255)
        im.save("out.png", 'png')
        
    def _testTxtRect(self):
        import Image,ImageDraw
        im2 = Image.new("L",(self.w,self.h),0)
        draw2 = ImageDraw.Draw(im2)
        fsize = self.GetFontSize("hehe")
        self.__off=20
        for i in range(8):
            r = self.__GetTxtRect([self.w/2,self.h/2], i, fsize)
            draw2.polygon([r[0],r[1],r[0]+r[2],r[1], \
                    r[0]+r[2],r[1]+r[3],r[0],r[1]+r[3]],fill=100+15*i)
            draw2.text([r[0],r[1]], str(i) )
        im2.save("lab.png", 'png')
        

    def GetFontSize(self, text, symbol=None):
        """获取某种字体的字符串的大小
        """
        if symbol is None:
            return self.__fontu.GetFontSize(text)
        else:
            dc = symbol['dc']
            fontclass=symbol['fontclass']
            fontu = fontclass(symbol,dc)
            return fontu.GetFontSize(text)

    def __GetTxtRect(self,ppos, pos, fsize):
        if ppos[0]<self.__dcl or ppos[0]>self.__dcr \
                or ppos[1]<self.__dct or ppos[1]>self.__dcb:
            return None
        elif pos == 0:#right
            return (ppos[0]+self.__off, ppos[1]-fsize[1]/2, \
                    fsize[0], fsize[1])
        elif pos == 1:#top
            return (ppos[0]-fsize[0]/2, ppos[1]-fsize[1]-self.__off, \
                    fsize[0], fsize[1])
        elif pos == 2:#left
            return (ppos[0]-fsize[0]-self.__off, ppos[1]-fsize[1]/2, \
                    fsize[0], fsize[1])
        elif pos == 3:#bottom
            return (ppos[0]-fsize[0]/2, ppos[1]+self.__off, \
                    fsize[0], fsize[1])
        elif pos == 4:#right top
            return (ppos[0]+self.__off, ppos[1]-fsize[1]-self.__off, \
                    fsize[0], fsize[1])
        elif pos == 5:#left top
            return (ppos[0]-self.__off-fsize[0], ppos[1]-fsize[1]-self.__off, \
                    fsize[0], fsize[1])
        elif pos == 6:#left bottom
            return (ppos[0]-fsize[0]-self.__off, ppos[1]+self.__off, \
                    fsize[0], fsize[1])
        elif pos == 7:#right bottom
            return (ppos[0]+self.__off, ppos[1]+self.__off, \
                    fsize[0], fsize[1])
        else:
            return None


    def __IsRectRight(self,r):
        #print r , self.__dcrect
        if r[0]<self.__dcl or r[0]+r[2]>=self.__dcr \
                or r[1]<self.__dct or r[1]+r[3]>=self.__dcb:
            return False
        else:
            #print r[0],r[0]+r[2],r[1],r[1]+r[3]
            if sum(sum(self.__canv[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]))==0:
                return True
            else:
                return False

    def __WriteRect(self, r, _dc=None):
        orip = [r[0],r[1]]
        mask = self.__mask[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]
        nu.put(self.__canv, mask, 1)
        if _dc:
            _dc.polygon([r[0],r[1],r[0]+r[2],r[1], \
                    r[0]+r[2],r[1]+r[3],r[0],r[1]+r[3]],fill=122)
        return orip

    def __LayoutP(self,ps,_dc=None):
        if not len(ps):
            return []
        canv = self.__canv
        size = self.w*self.h
        basep = []
        for labp in ps:
            basep+=labp[1]
        #首先把所有点都标上
        a = [p[0][1]*self.w+p[0][0] for p in basep \
                if 0<p[0][0]<self.w and 0<p[0][1]<self.h]
        nu.put(canv,a, 1)#put all points

        ret = []
        for labp in ps:
            self.symbol = symbol = labp[0]
            points = labp[1]
            self.__fontu = self.__fontclass(symbol,self.__dc)
            for p in points:
                txt = p[1]
                fsize = self.GetFontSize(txt)
                ppos = p[0]
                r = None
                for pos in range(8):
                    r = self.__GetTxtRect(ppos, pos, fsize)
                    if r is None:
                        break
                    if self.__IsRectRight(r):
                        break
                    elif pos == 7:
                        r = None
                if r is not None:
                    ret.append([self.__WriteRect(r,_dc),txt,symbol])
        return ret
            
    def __LayoutPL(self, ps, _dc=None):
        if not len(ps):
            return []
        canv = self.__canv
        size = self.w*self.h
        #a = [p[1]*self.w+p[0] for p in ps if 0<p[0]<self.w and 0<p[1]<self.h]
        #nu.put(canv,a, 1)#put all points

        ret = []
        for labp in ps:
            self.symbol = symbol = labp[0]
            pls = labp[1]
            self.__fontu = self.__fontclass(symbol,self.__dc)
            for p in pls:
                txt = p[1]
                fsize = self.GetFontSize(txt)
                ppos = p[0]
                r = self.__GetTxtCenterRect(ppos, fsize)
                if not self.__IsRectCenterRight(r):
                    r=None
                if r is not None:
                    ret.append([self.__WriteRect(r,_dc),txt,symbol])
        return ret

    def __GetTxtCenterRect(self, ppos, fsize):
        if ppos[0]<self.__dcl or ppos[0]>self.__dcr \
                or ppos[1]<self.__dct or ppos[1]>self.__dcb:
            return None
        else:
            return (int(ppos[0]-fsize[0]/2), int(ppos[1]-fsize[1]/2), \
                    fsize[0], fsize[1])

    def __IsRectCenterRight(self, r):
        if r is None:
            return False
        if r[0]<self.__dcl or r[0]+r[2]>=self.__dcr \
                or r[1]<self.__dct or r[1]+r[3]>=self.__dcb:
            return False
        else:
            #print r[0],r[0]+r[2],r[1],r[1]+r[3]
            if sum(sum(self.__canv[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]))==0:
                return True
            else: return False

    def __LayoutL(self, lines, _dc=None):
        if not len(lines):
            return []
        canv = self.__canv
        size = self.w*self.h
        ret = []
        for labl in lines:
            self.symbol = symbol = labl[0]
            ls = labl[1]
            self.__fontu = self.__fontclass(symbol,self.__dc)
            for line in ls:
                txt = line[1]
                lp = line[0]
                self.__GetBestLinePos( lp, txt, ret, _dc)
        return ret

    def __GetBestLinePos(self, lineParser, word, ret, _dc):
        letters = cz_split(word)
        midp1,midp2 = lineParser.GetLongestPart()
        fsizes = []
        for letter in letters:
            fsizes.append(self.GetFontSize(letter))
        fsteps = [i[0]+5 for i in fsizes]
        points = SplitLine(midp1,midp2,fsteps)
        points = [[int(x),int(y)] for x,y in points]
        rs = []
        for i in range(len(points)):
            ppos = points[i]
            letter = letters[i]
            r = self.__GetTxtCenterRect(ppos, fsizes[i])
            if not self.__IsRectCenterRight(r):
                r=None
            rs.append(r)
        if None not in rs:
            for i in range(len(points)):
                r = rs[i]
                letter = letters[i]
                ret.append([self.__WriteRect(r,_dc), letter, self.symbol])
            

if __name__=="__main__":
    import wx
    from random import randint
    from geosings.ui.core.wxFont import *
    from Symbol import GetDefTextSymbol,TextSymConfKeys
    app = wx.PySimpleApp()
    rect = (500,300)
    r = wx.Rect(0,0,rect[0],rect[1])
    count = 130
    off = 3
    points = [[[randint(0,rect[0]-1),randint(0,rect[1]-1)],"hehe"] for i in range(count)]
    texts = [u"hehe" for i in range(count)]
    font = GetDefaultFont()
    symbols = {"dc":None,
            "fontclass":FontUtils,
            "points":[[GetDefTextSymbol(),points]],
            "off":off,
            "polygons":[],
            "lines":[],
            }
    sl = LabelLayout(symbols, r)
    #print sl.Layout()
    sl._output()
    sl._testTxtRect()

