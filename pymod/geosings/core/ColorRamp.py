# -*- coding: utf-8 -*-
"""该模块定义颜色预定义带

 - writer:linux_23; create:2008.5.5; version:1; 创建
"""

import Image, ImageDraw,math

class ColorRamp:
    """预定义颜色带
    """
    def __init__(self,conf={
        'ps':[(255,0,0),(255,255,100),(255,255,0),(39,170,39), \
        (0,255,0),(0,255,255),(130,150,150),(0,0,33),(39,39,77,150)],
        }, name=None, step=25, a=150):
        self.a = a
        self.conf = conf
        self.count = len(self.conf['ps'])-1
        self.r = self.conf['ps'][0][0]
        self.rstep = (self.conf['ps'][1][0]-self.r)
        self.g = self.conf['ps'][0][1]
        self.gstep = (self.conf['ps'][1][1]-self.g)
        self.b = self.conf['ps'][0][2]
        self.bstep = (self.conf['ps'][1][2]-self.b)
        maxstep = max(math.fabs(self.rstep), math.fabs(self.gstep), math.fabs(self.bstep))
        self.rstep /= maxstep
        self.gstep /= maxstep
        self.bstep /= maxstep
        self.i = 0
        self.step = 0
        self.name = name
        if name is not None:
            self.output(self.name)
        self.index = 0
        self.stepc = step
        
        self.random_i = 0
        self.random_k = 0
    def set_step(self, step):
        """设置下一个颜色的跨度
        """
        self.stepc = step

    def output(self, name):
        """把颜色带保存成png文件
        """
        self.colorlist = []
        color = self._next_color()
        while color:
            self.colorlist.append(color)
            color = self._next_color()
        self.im = Image.new("RGBA",(len(self.colorlist),30),(255,255,255,100))
        #print self.colorlist
        draw = ImageDraw.Draw(self.im)
        i = 0
        for color in self.colorlist:
            color = (color[0],color[1],color[2],self.a)
            #print color
            draw.line((i,0, i,30), fill=color)
            i+=1
        del draw
        #print 'save to png'
        self.im.save(name+".png", "png")

    def next_color(self):
        """下种颜色
        """
        if self.name:
            if self.index < len(self.colorlist):
                c = self.im.getpixel((self.index,10))
                #print self.index
                self.index+=self.stepc
                return c
            else:
                return None
        else:
            return self._next_color()

    def random_color(self):
        """随机颜色(其实并不随机，需要保证最大差异)
        """
        if self.random_k == 0:
            if self.random_i == 0:
                self.random_i=1
                return self.conf['ps'][0]
            else:
                self.random_k = 1
                self.random_i = 0
                return self.conf['ps'][-1]
        else:
            if self.random_k == self.random_i:
                self.random_k*=2
                self.random_i=0
            at = self.im.size[0]*1.0/self.random_k*(self.random_i+0.5)
            c = self.im.getpixel((int(at),10))
            #print c
            self.random_i+=1
            return c

    def reset_random(self):
        """重设随机颜色
        """
        self.random_i = 0
        self.random_k = 0

    def _next_color(self):
        self.r += self.rstep
        self.g += self.gstep
        self.b += self.bstep

        nowbc = self.conf['ps'][self.step]
        nowec = self.conf['ps'][self.step+1]
        
        if math.fabs(self.r-nowbc[0]) >= math.fabs(nowec[0]-nowbc[0]) and \
            math.fabs(self.g-nowbc[1]) >= math.fabs(nowec[1]-nowbc[1]) and \
            math.fabs(self.b-nowbc[2]) >= math.fabs(nowec[2]-nowbc[2]):
            self.step += 1
            if self.step<self.count:
                self.r = self.conf['ps'][self.step][0]
                self.g = self.conf['ps'][self.step][1]
                self.b = self.conf['ps'][self.step][2]
                self.rstep = (self.conf['ps'][self.step+1][0]-self.r)
                self.gstep = (self.conf['ps'][self.step+1][1]-self.g)
                self.bstep = (self.conf['ps'][self.step+1][2]-self.b)
                #print self.rstep,self.gstep,self.bstep
                maxstep = max(math.fabs(self.rstep),
                        math.fabs(self.gstep), 
                        math.fabs(self.bstep))
                self.rstep /= (maxstep*1.0)
                self.gstep /= (maxstep*1.0)
                self.bstep /= (maxstep*1.0)
            else:
                return None
        return (int(self.r),int(self.g),int(self.b))


rainbow = ColorRamp(
            name="rainbow"
        )
