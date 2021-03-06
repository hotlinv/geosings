# -*- coding: utf-8 -*-
"""
该模块定义地理画板控件

 - writer:linux_23; create: 2008.4.13; version:1; 创建

"""
import wx,math

from geosings.core.GeoRect import GeoRect
from geosings.core.system import ScreenPToGeoP,choose,ExtGeoRect
from geosings.ui.core.UIConst import *
from geosings.core.system.GLog import *
#from geosings.ui.UISettings import *

class OperHandler:
    def __init__(self, ctrl):
        self.ctrl = ctrl
    def OnChar(self, evt):pass
    def ReSize(self,evt): pass
    def OnLeftDown(self, evt):pass
    def OnLeftUp(self, evt):pass
    def OnMotion(self, evt):pass
    def OnBDraw(self, dc):pass
    def OnEDraw(self, dc):pass

class ModeOperHandler(OperHandler):
    def __init__(self, ctrl, mode=None):
        OperHandler.__init__(self, ctrl)
        self.__mode = mode
    def GetMode(self):
        return self.__mode

class NoModeHandler(ModeOperHandler):
    def __init__(self, ctrl):
        ModeOperHandler.__init__(self, ctrl, ModeKey.NoneMode)
        debug("mode: no")

class PointWhereHandler(OperHandler):
    def __init__(self,ctrl):
        OperHandler.__init__(self, ctrl)
    def OnMotion(self, evt):
        info("X: %s, Y: %s", evt.GetX(), evt.GetY())

class RectHandler(ModeOperHandler):
    """橡皮筋矩形操作
    """
    def __init__(self,ctrl,mode=None):
        ModeOperHandler.__init__(self, ctrl, mode)
        self.isDraging = 0
        self.tmpxb = 0 #mouse begin x
        self.tmpyb = 0 #mouse begin y
        self.tmpxe = 0 #mouse end x
        self.tmpye = 0 #mouse end y
        
    def OnMotion(self, evt):
        p = evt.GetPosition()
        if self.isDraging:
            self.__DragingRect(p)
    def OnLeftDown(self, evt):
        p = evt.GetPosition()
        self.__DragRectBegin(p)
    def OnLeftUp(self, evt):
        p = evt.GetPosition()
        self.__DragRectEnd(p)

    def __DragRectBegin(self,mousep):
        """拖拽矩形框开始
        @type mousep: wxMouse
        @param mousep: 拖拽矩形的开始点
        """
        self.isDraging = 1
        self.tmpxb = mousep.x; self.tmpyb = mousep.y
        self.tmpxe = mousep.x; self.tmpye = mousep.y

    def __DragingRect(self,mousep):
        """拖拽矩形中
        @type mousep: wxMouse
        @param mousep: 拖拽到了什么位置？
        """
        dc = wx.ClientDC(self.ctrl)
        dc.SetLogicalFunction(wx.XOR)
        self.__DrawRect(dc,self.tmpxb,self.tmpyb,x2=self.tmpxe,y2=self.tmpye,color=wx.WHITE)
        self.tmpxe = mousep.x;self.tmpye=mousep.y
        self.__DrawRect(dc,self.tmpxb,self.tmpyb,x2=self.tmpxe,y2=self.tmpye,color=wx.WHITE)
        dc.SetLogicalFunction(wx.COPY)

    def __DragRectEnd(self,mousep):
        """拖拽结束
        @type mouse: wxMouse
        @param mouse: 什么位置结束
        """
        self.isDraging = 0
        dc = wx.ClientDC(self.ctrl)
        self.tmpxe = mousep.x;self.tmpye=mousep.y
        dc.SetLogicalFunction(wx.XOR)
        self.__DrawRect(dc,self.tmpxb,self.tmpyb,x2=self.tmpxe,y2=self.tmpye,color=wx.WHITE)
        dc.SetLogicalFunction(wx.COPY)
    def __DrawRect(self,dc,x,y,w=None,h=None,x2=None,y2=None, \
            color=wx.BLACK,linew=1,brush=wx.TRANSPARENT_BRUSH):
        """绘制矩形
        @type dc: wxDC
        @param dc: 绘制DC
        @type x,y: int
        @param x,y: 绘制起始位置
        @type w,h: int
        @param w,h: 绘制的宽高（可以和后面的x2,y2互选)
        @type x2,y2: int
        @param x2,y2: 绘制的终止位置(该参数组和前面的wh是互斥的)
        @type color: wxColour
        @param color: 绘制颜色(外框)
        @type linew: int
        @param linew: 线宽
        @type brush: wxBrush
        @param brush: 填充颜色的画刷
        """
        peno = dc.GetPen()
        brusho = dc.GetBrush()
        pen = wx.Pen(color,linew,wx.SOLID)
        dc.SetPen(pen)
        #brush2 = wx.Brush(wx.Colour(255,255,12,77))
        dc.SetBrush(brush)
        if w is not None and h is not None:
            dc.DrawRectangle(x,y,w,h)
        if x2 is not None and y2 is not None:
            w = math.fabs(x-x2)
            h = math.fabs(y-y2)
            x = choose(x>x2,x2,x)
            y = choose(y>y2,y2,y)
            dc.DrawRectangle(x,y,w,h)
        dc.SetPen(peno)
        dc.SetBrush(brusho)

class PanHandler(ModeOperHandler):
    def __init__(self, ctrl):
        ModeOperHandler.__init__(self, ctrl, ModeKey.PanMode)
    def OnLeftDown(self, evt):
        map = self.ctrl.map
        if self.ctrl.geoext is None:
            return
        rect = self.ctrl.GetClientRect()
        gx,gy = ScreenPToGeoP(evt.GetX(), evt.GetY(), \
                rect, self.ctrl.geoext)
        gwidth = self.ctrl.geoext.GetWidth()
        gheight = self.ctrl.geoext.GetHeight()

        nowext = GeoRect(gx-gwidth/2.0, gy-gheight/2.0,
                gx+gwidth/2.0, gy+gheight/2.0)

        self.ctrl.geoext.Set(nowext)
        self.ctrl.ReDraw()

class InfoHandler(ModeOperHandler):
    def __init__(self, ctrl):
        ModeOperHandler.__init__(self, ctrl, ModeKey.InfoMode)
    def OnLeftDown(self, evt):
        from geosings.ui.PyMainPanel import GetMainPanel
        map = self.ctrl.map
        p = evt.GetPosition()
        notebook = GetMainPanel().nb
        for i in range(notebook.GetPageCount()):
            if notebook.GetPageText(i)==_("Attribute"):
                notebook.SetSelection(i)
        if len(self.ctrl.map.GetSelectedLayersItems())>0:
            dcrect = self.ctrl.GetClientRect()
            if self.ctrl.geoext is not None:
                GetMainPanel().infoPanel.RegHLDrawFoo(self.ctrl.WinkFeatures)
                fs = self.ctrl.map.GetFeaturesByPoint((p.x,p.y),dcrect,self.ctrl.geoext)
                GetMainPanel().infoPanel.SetFeatures(fs)
            self.ctrl.SetFocus()
        else:
            error(_("you should select a layer as hightlight"))

        #self.ctrl.ReDraw()

class ZoomInHandler(RectHandler):
    def __init__(self, ctrl):
        RectHandler.__init__(self, ctrl, ModeKey.ZoomInMode)
        self.bgx = None
        self.bgy = None
    def OnLeftDown(self, evt):
        RectHandler.OnLeftDown(self, evt)
        rect = self.ctrl.GetClientRect()
        self.bgx, self.bgy = ScreenPToGeoP(evt.GetX(), evt.GetY(), \
                rect, self.ctrl.geoext)
    def OnLeftUp(self, evt):
        RectHandler.OnLeftUp(self, evt)
        rect = self.ctrl.GetClientRect()
        gwidth = self.ctrl.geoext.GetWidth()
        gheight = self.ctrl.geoext.GetHeight()
        egx, egy = ScreenPToGeoP(evt.GetX(), evt.GetY(), \
                rect, self.ctrl.geoext)
        if self.bgx==egx or self.bgy==egy:
            return
        nowext = GeoRect(self.bgx, self.bgy, egx, egy)
        nowext = ExtGeoRect(nowext, rect.GetWidth(), rect.GetHeight())
        self.ctrl.geoext.Set(nowext)
        self.ctrl.ReDraw()

class ZoomOutHandler(RectHandler):
    def __init__(self, ctrl):
        RectHandler.__init__(self, ctrl, ModeKey.ZoomOutMode)
        self.bgx = None
        self.bgy = None
    def OnLeftDown(self, evt):
        RectHandler.OnLeftDown(self, evt)
        rect = self.ctrl.GetClientRect()
        self.bgx, self.bgy = ScreenPToGeoP(evt.GetX(), evt.GetY(), \
                rect, self.ctrl.geoext)
    def OnLeftUp(self, evt):
        RectHandler.OnLeftUp(self, evt)
        rect = self.ctrl.GetClientRect()
        gwidth = self.ctrl.geoext.GetWidth()
        gheight = self.ctrl.geoext.GetHeight()
        egx, egy = ScreenPToGeoP(evt.GetX(), evt.GetY(), \
                rect, self.ctrl.geoext)
        if self.bgx==egx or self.bgy==egy:
            return
        inext = GeoRect(self.bgx, self.bgy, egx, egy)
        inext = ExtGeoRect(inext, rect.GetWidth(), rect.GetHeight())
        scale = gwidth*1.0/inext.GetWidth()
        midgx, midgy = inext.GetMiddlePoint()
        midrx, midry = self.ctrl.geoext.GetMiddlePoint()
        nmidgx = midrx-(midgx-midrx)*scale
        nmidgy = midry+(midry-midgy)*scale
        xw = gwidth*scale/2.0
        xh = gheight*scale/2.0
        nowext = GeoRect(nmidgx-xw,nmidgy+xh,nmidgx+xw,nmidgy-xh)
        self.ctrl.geoext.Set(nowext)
        self.ctrl.ReDraw()

class CharHandler(OperHandler):
    def __init__(self,ctrl):
        OperHandler.__init__(self, ctrl)
    def OnChar(self, evt):
        from geosings.ui.core.wxKeyParser import KeyParser
        kp = KeyParser(evt)
        keycode = kp.keycode
        keyname = kp.keyname
        self.SentOrder(keyname,keycode)
    def SentOrder(self,keyname="",keycode=0):
        """命令分发
        @type keyname: str
        @param keyname: 命令名
        @type keycode: int
        @param keycode: 命令码
        """
        #from UISettings import MSGKEY
        from geosings.core.system.GssConfDict import GSSMSGS as MSGKEY
        from geosings.ui.PyMainPanel import GetMainPanel
        debug("sent order: %s %s", keyname, keycode)
        if keycode==58:# ':' input the order
            #self.EnableInput(True)
            GetMainPanel().EnableInput(True)
            pass
        elif keyname==MSGKEY["MSG_KEY_MODE_ZOOMIN"]: #大写表示放大
            self.ctrl.RegHandler(ZoomInHandler(self.ctrl))
        elif keyname==MSGKEY["MSG_KEY_MODE_ZOOMOUT"]: #小写表示缩小
            self.ctrl.RegHandler(ZoomOutHandler(self.ctrl))
        elif keyname == MSGKEY["MSG_KEY_MODE_NO"]:
            self.ctrl.RegHandler(NoModeHandler(self.ctrl))
        elif keyname == MSGKEY["MSG_KEY_MODE_PAN"]:
            self.ctrl.RegHandler(PanHandler(self.ctrl))
        elif keyname == MSGKEY["MSG_KEY_MODE_INFO"]:
            self.ctrl.RegHandler(InfoHandler(self.ctrl))
        elif keycode==27 or keyname==MSGKEY["MSG_KEY_DRAW"]:
            self.ctrl.ReDraw()
        elif keyname==MSGKEY["MSG_KEY_FULL"]:
            self.ctrl.geoext = None
            self.ctrl.ReDraw()

