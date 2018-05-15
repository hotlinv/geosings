# -*- coding: utf-8 -*-
"""
该模块定义画板控件基类

 - writer:linux_23; create: ; version:1; 创建
 - linux_23: 2007.9.15; 添加闪动效果代码
 - linux_23: 2007.9.17; 添加聚焦点的很酷的效果
 - linux_23: 2007.11.28; 添加透明效果
"""
import wx,math,ogr
from copy import deepcopy

from geosings.core.gssconst import FeatureType
from geosings.core.GeomWkt import *
from geosings.core.system import ScreenPToGeoP,choose
from geosings.core.GeoRect import GeoRect

from geosings.ui.core.UIConst import *
from geosings.ui.core.Document import mainDocument
from geosings.ui.commondlg.FeatureTabPanel import FeatureTabFrame

from LayerCanvas import LayerCanvas,LabelCanvas,HLLayerCanvas,FeaturesCanvas
from geosings.core.GLog import *

def GDC(dc):
    try:
        return wx.GCDC(dc)
    except NotImplementedError:
        return dc

class Feature:
    """Geosings的要素类
    """
    def __init__(self,featuretype,obj):
        """初始化函数
        @type featuretype: int
        @param featuretype: 要素类型
        @type obj: GDAL Feature
        @param obj: 实际的Feature对象
        """
        self.featuretype = featuretype
        self.__obj = obj

class MyCanvas(wx.Panel):
    """主画板类
    """
    def __init__(self, parent,mainctrl,oparea):
        """初始化
        @type parent: wxCtrl
        @param parent: 父控件
        @type mainctrl: wxCtrl
        @param mainctrl: 主程序
        @type oparea: wxCtrl
        @param oparea: 输出控件
        """
        wx.Panel.__init__(self,parent,-1,style=wx.WANTS_CHARS)
        self.oparea = oparea
        self.oparea.Init(self)
        self.parent = parent
        self.mainctrl = mainctrl
        self.SetBackgroundColour(wx.WHITE)
        self.maxWidth  = 1000
        self.maxHeight = 1000
        self.mousep = wx.Point(0,0)
        self.mousesel = wx.Point(0,0)
        self.mousesel2 = wx.Point(-1,-1)
        self.flag2 = 0
        self.action2 = 0
        self.mode = ModeKey.NoneMode
        mainDocument.geoext = deepcopy(mainDocument.map.allGeoExt)
        self.map = mainDocument.map
        
        self.tmpxb = 0 #mouse begin x
        self.tmpyb = 0 #mouse begin y
        self.tmpxe = 0 #mouse end x
        self.tmpye = 0 #mouse end y
        self.isDraging = 0 # is draging?
        
        self.lc = None # LayerCanvas
        self.rd = 1 # ReDraw?

        self.ftabFrame = None
        try:
            pass
            self.ftabFrame = FeatureTabFrame(self,-1,
                    "selection features",
                    style=wx.CAPTION | wx.STAY_ON_TOP |wx.RESIZE_BORDER ,
                    size=((350,200)))
            self.ftabFrame.SetDrawFoo(self.WinkFeatures)
        except:
            log( 'load FeatureTabDialog false','X'*20)
 
        #self.InitOutputCanvas()

        cursor = wx.StockCursor(wx.CURSOR_CROSS)
        self.SetCursor(cursor)
        
        self.InitBuffer()
        #self.dc = None
        
        # Bind event handle to Function
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.ReSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.__do_layout()


    #def GetCDC(self):
    #    if self.dc is None:
    #        return wx.ClientDC(self)
    #    else:
    #        return self.dc


    def WinkFeatures(self,features):
        """闪动某（些）要素
        @type features: list
        @param features: 要闪动的要素集合
        """
        dc = wx.ClientDC(self)
        fc = FeaturesCanvas(features)
        fc.SetWink(10)
        fc.BindAimFoo(self.Aim)
        rect = self.GetClientRect()
        igeoext = mainDocument.geoext
        fc.Draw(dc,rect,igeoext)
        

    def ShowFTable(self,show):
        """（不）显示选择选中的对象的属性
        @type show: bool
        @param show: 要不要显示
        """
        pass
        if self.ftabFrame is None:
            return
        if show:
            self.ftabFrame.Show(True)
            pass
        else:
            self.ftabFrame.Show(False)
            pass

    def InitBuffer(self):
        """因为采用双缓存，所以要对缓存进行初始化
        """
        size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        #dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.SetBackground(wx.Brush(GSSCONF["CANV_BACKGROUND_COLOR"]))
        dc.Clear()
        self.PrepareDC(dc)
        #self.DrawLines(dc)
        self.DoDrawing(dc)
        self.rd = 0

    def __do_layout(self):
        """对画板内的空间分布进行排列
        """
        self.oparea.InitLayout()
        self.Layout()

    def OnPaint(self, evt):
        """需要重绘时响应的事件
        @type evt: wxEvent
        @param evt: wxEVT_PAINT事件
        """
        #dc = wx.PaintDC(self)
                # since we're not buffering in this case, we have to
        # paint the whole window, potentially very time consuming.
        #if self.rd:
        dc = wx.BufferedPaintDC(self,self.buffer)
        #pass
        #else:
        #    dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        #    dc.Clear()

        #    self.PrepareDC(dc)

        #    self.DoDrawing(dc)
        #    self.rd = 0

    def DoDrawing(self, dc, all=False):
        """进行重绘操作时的主要函数
        @type dc: wxDC
        @param dc: 绘制环境
        @type all: bool
        @param all: 要不要绘制所有范围(默认为否)
        """
        dc.BeginDrawing()
        rect = self.GetClientRect()
        #dc.SetDeviceOrigin(0,rect.GetHeight()-20)
        if all:#如果要画超过屏幕范围的所有数据
            nowgeoext = mainDocument.geoext
            allgeoext = self.map.allGeoExt
            dcrect = rect
            allw = allgeoext.GetWidth()/nowgeoext.GetWidth()*dcrect.GetWidth()
            allh = allgeoext.GetHeight()/nowgeoext.GetHeight()*dcrect.GetHeight()
            rect = GeoRect(0,0,allw,allh)
            igeoext = allgeoext
        else:
            if mainDocument.zoomall and len(self.map.layers)>0:# 如果放大到全图到屏幕
                debug("zoom to all")
                mainDocument.initGeoExt(rect.GetWidth(),rect.GetHeight())
                mainDocument.geoext = deepcopy(self.map.allGeoExt)
            igeoext = mainDocument.geoext
        self.labelCanvas = LabelCanvas()
        for layer in self.map.layers:
            if layer is not None and layer.visual:
                self.__DrawLayer(dc,layer,rect,igeoext)
        if self.map.whereFlite != "":
            sellyr = self.map.GetLayer(self.map.whereLayer)
            hlcanv = HLLayerCanvas(sellyr)
            hlcanv.SetWhereFilter(self.map.whereFlite,self.map.codec)
            hlcanv.Draw(dc,rect,igeoext)
        self.labelCanvas.Draw(dc,rect,igeoext)
        if not all:
            self.__DrawCross(dc,rect.GetWidth()/2,rect.GetHeight()/2,wx.RED)
        dc.EndDrawing()

    def __DrawLayer(self,dc,layer,wprect,georect):
        """绘制图层
        @type dc: wxDC
        @param dc: 绘制DC
        @type layer: L{geosings.core.Layer.Layer}
        @param layer: 要绘制的图层
        @type wprect: L{geosings.core.GeoRect.GeoRect}
        @param wprect: 可绘制的屏幕矩形
        @type georect: L{geosings.core.GeoRect.GeoRect}
        @param georect: 可绘制的屏幕范围内的地理范围矩形
        """
        lc = LayerCanvas.Create(layer)
        lc.labelCanvas = self.labelCanvas
        lc.Draw(dc,wprect,georect)
        #mainDocument.geoext = mainDocument.geoext
            
    #def ReDrawLayer(self):
    #    print 'redrawlayer'
    #    dc = wx.BufferedDC(wx.ClientDC(self),self.buffer)
    #    #dc.SetPen(wx.RED)
    #    rect = self.GetClientRect()
    #    for layer in self.map.layers:
    #        if layer is not None:
    #            self.__DrawLayer(dc,layer,rect)
    #    self.__DrawCross(dc,rect.GetWidth()/2,rect.GetHeight()/2,
    #        wx.RED)


    def SendMessage(self,msg):
        """画布要向外发送信息
        @type msg: str
        @param msg: 向外发送的信息
        """
        from geosings.ui.core.Brain import msgParser
        msgParser.SendMsg(msg)
        result = msgParser.result
        if result==ActionResult.UpdateAll:
            #self.Refresh()
            self.ReDraw()
        else: return result

    def SendOrder(self,order,*arrs):
        """画布要向外发送的命令
        @type order: str
        @param order: 向外发送的命令
        """
        from geosings.ui.core.Brain import msgParser
        msgParser.SendOrder(order,arrs)
        result = msgParser.result
        if result==ActionResult.UpdateAll:
            #self.Refresh()
            self.ReDraw()
        else: return ActionResult.Failuse

    def SetMode(self,mode):
        """将画布设置成某个状态
        @type mode: ModeKey
        @param mode: 要将画布设置的状态
        """
        self.mode = mode
        if mode == ModeKey.InfoMode:
            self.ShowFTable(True)
        else:
            self.ShowFTable(False)
        self.SetFocus()

    def OnChar(self, evt):
        """键盘响应
        @type evt: wxEvent
        @param evt: wxEVT_CHAR事件
        """
        self.mainctrl.EvtOrder(evt)        
            
    def ZoomToAll(self):
        """把图层放大到全图可见
        """
        mainDocument.ReInitGeoExt()
        mainDocument.geoext = deepcopy(mainDocument.map.allGeoExt)
        self.ReDraw()

    def ReDraw(self):
        """重新绘制当前屏幕的区域
        """
        self.flag2 = 0
        self.mousesel2.x = -1
        self.mousesel2.y = -1
        self.action2 = 0
        self.rd = 1
        self.InitBuffer()
        self.Refresh(True)
        #self.ReDrawLayer()

    def OnIdle(self,evt):
        """没有操作时进行的响应
        @type evt: wxEvent
        @param evt: EVT_IDLE事件
        """
        #print self.rd
        if self.rd:
            self.InitBuffer()
            self.Refresh(True)

    def ReSize(self,evt):
        """窗口重新设置大小时的响应
        @type evt: wxEvent
        @param evt: EVT_SIZE事件
        """
        #self.ReDraw()
        self.rd = 1
        #self.ReDraw()
        self.Layout() #重新排列上面的组件

    def Pan(self,keyname,x=0,y=0,movlen=mainDocument.panStep):
        """漫游的响应事件(键盘对漫游操作的响应)
        @type keyname: str
        @param keyname: 按键名称
        @type x,y: int
        @param x,y: 废弃(可以从当前获得屏幕中心位置点)
        @type movlen: int
        @param movlen: 按键按下后需要移动的步长
        """
        from geosings.core.GssConfDict import GSSMSGS as MSGKEY
        #geoext = mainDocument.geoext
        dcrect = self.GetClientRect()
        if mainDocument.geoext is not None:
            if keyname == MSGKEY["MSG_KEY_MODE_PAN"]:
                midx,midy = mainDocument.geoext.GetMiddlePoint()
                mtopx,mtopy = ScreenPToGeoP(x,y,dcrect,mainDocument.geoext)
                xx = mtopx-midx
                xy = mtopy-midy
            elif keyname == MSGKEY["MSG_KEY_LEFT"]:
                mtopx,mtopy = ScreenPToGeoP(math.fabs(movlen),0, \
                        dcrect,mainDocument.geoext)
                xx = -(mtopx-mainDocument.geoext.GetLeft())
                xy = 0
            elif keyname == MSGKEY["MSG_KEY_RIGHT"]:
                mtopx,mtopy = ScreenPToGeoP(math.fabs(movlen),0, \
                        dcrect,mainDocument.geoext)
                xx = mtopx-mainDocument.geoext.GetLeft()
                xy = 0
            elif keyname == MSGKEY["MSG_KEY_DOWN"]:
                mtopx,mtopy = ScreenPToGeoP(0,math.fabs(movlen), \
                        dcrect,mainDocument.geoext)
                xx = 0
                xy = mtopy-mainDocument.geoext.GetTop()
            elif keyname == MSGKEY["MSG_KEY_UP"]:
                mtopx,mtopy = ScreenPToGeoP(0,math.fabs(movlen), \
                        dcrect,mainDocument.geoext)
                xx = 0
                xy = -(mtopy-mainDocument.geoext.GetTop())
            nowleft = mainDocument.geoext.GetLeft()+xx
            nowright = mainDocument.geoext.GetRight()+xx
            nowtop = mainDocument.geoext.GetTop()+xy
            nowbottom = mainDocument.geoext.GetBottom()+xy
            mainDocument.geoext.ReSet(nowleft,nowtop,nowright,nowbottom)
            mainDocument.zoomall = 0
            #self.Refresh()
            self.ReDraw()

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
        dc = wx.ClientDC(self)
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
        dc = wx.ClientDC(self)
        self.tmpxe = mousep.x;self.tmpye=mousep.y
        dc.SetLogicalFunction(wx.XOR)
        self.__DrawRect(dc,self.tmpxb,self.tmpyb,x2=self.tmpxe,y2=self.tmpye,color=wx.WHITE)
        dc.SetLogicalFunction(wx.COPY)

    def OnLeftDown(self, evt):
        """鼠标左键按下的响应函数
        @type evt: wxEvent
        @param evt: 鼠标事件
        """
        self.SetFocus()
        p = evt.GetPosition()
        dc = wx.ClientDC(self)
        from geosings.core.GssConfDict import GSSMSGS as MSGKEY
        if self.mode == ModeKey.PanMode:
            self.Pan(MSGKEY["MSG_KEY_MODE_PAN"],p.x,p.y)
        elif self.mode == ModeKey.ZoomOutMode or \
                self.mode == ModeKey.ZoomInMode:
            self.__DragRectBegin(p)
        elif self.mode == ModeKey.InfoMode:
            if len(mainDocument.map.GetSelectedLayersItems())>0:
                self.GetFeaturesInfo(p)
                self.SetFocus()
            else:
                err(_("you should select a layer as hightlight"))

    def GetFeaturesInfo(self,point):
        """获取选取对象的信息
        @type point: wxPoint
        @param point: 选取对象时的点(这里需要改进得更加通用)
        """
        if self.ftabFrame is None:
            return 
        dcrect = self.GetClientRect()
        if mainDocument.geoext is not None:
            #px,py = ScreenPToGeoP(point.x-2,point.y-2,dcrect,mainDocument.geoext) 
            #p2x,p2y = ScreenPToGeoP(point.x+2,point.y+2,dcrect,mainDocument.geoext)
            #wkt = CreatePolygonWkt([[px,py],
            #    [px,p2y],[p2x,p2y],[p2x,py],[px,py]])
            #print wkt
            #geop = ogr.CreateGeometryFromWkt(wkt)
            #fs = mainDocument.GetFeaturesByGeometry(geop)
            fs = mainDocument.map.GetFeaturesByPoint((point.x,point.y),dcrect,mainDocument.geoext)
            self.ftabFrame.SetFeatures(fs)

    def OnLeftUp(self, evt):
        """鼠标松开的时候的响应
        @type evt: wxEvent
        @param evt: 鼠标事件
        """
        p = evt.GetPosition()
        if self.mode == ModeKey.ZoomOutMode or \
                self.mode == ModeKey.ZoomInMode:
            self.__DragRectEnd(p)
            self.Zoom(self.mode)

    def OnMotion(self, evt):
        """鼠标移动的相应事件
        @type evt: wxEvent
        @param evt: 鼠标事件
        """
        self.mousep.x = evt.GetX()
        self.mousep.y = evt.GetY()
        if mainDocument.geoext is not None:
            #geoext = mainDocument.geoext
            rect = self.GetClientRect()
            dcw = rect.GetWidth()
            dch = rect.GetHeight()
            geox,geoy = ScreenPToGeoP(self.mousep.x,self.mousep.y, \
                    rect,mainDocument.geoext)
            self.mainctrl.PrintMouse(geox,geoy)
        else:
            self.mainctrl.PrintMouse(self.mousep.x,self.mousep.y)
        if self.isDraging:
            self.__DragingRect(evt.GetPosition())
     

    def __DrawFeatureFun(self,ftype):
        """在画布上绘制形状的函数(废弃)
        @type ftype: FeatureType
        @param ftype: 绘制形状的类型
        """
        if ftype == FeatureType.rect:
            return self.__DrawRect

    def __DrawCross(self,dc,px,py,color=wx.BLACK,linew=1,linelen=5):
        """在画布上画一个十字
        @type dc: wxDC
        @param dc: 绘制DC
        @type px,py: int
        @param px,py: 绘制位置
        @type color: wxColor
        @param color: 绘制颜色
        @type linew: int
        @param linew: 线宽
        @type linelen: int
        @param linelen: 线长
        """
        peno = dc.GetPen()
        pen = wx.Pen(color,linew,wx.SOLID)
        dc.SetPen(pen)
        dc.DrawLine(px-linelen,py,px+linelen+1,py)
        dc.DrawLine(px,py-linelen,px,py+linelen+1)
        dc.SetPen(peno)

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

    def __initZoomInRect(self,grect,dcw,dch):
        """获得调整后要放大的矩形范围（拉框的大小和屏幕大小不成比例）
        @type grect: L{geosings.core.GeoRect.GeoRect}
        @param grect: 拉框覆盖的地理范围矩形
        @type dcw,dch: int
        @param dcw,dch: 拉框的矩形的宽高
        @rtype: L{geosings.core.GeoRect.GeoRect}
        @return: 调整大小后需要绘制的地理区域矩形
        """
        grw = grect.GetWidth()*1.0
        grh = grect.GetHeight()*1.0
        grmx,grmy = grect.GetMiddlePoint()
        if grw*1.0/grh>dcw*1.0/dch:# 按宽来调整 
            grh = dch*1.0/dcw*grw    
        else:   # 按高调整
            grw = dcw*1.0/dch*grh
        return GeoRect(grmx-grw/2,grmy-grh/2,grmx+grw/2,grmy+grh/2)
    
    def __initZoomOutRect(self,grect,dcrect,mrect):
        """获得调整后要缩小的矩形范围（拉框的大小和屏幕大小不成比例）
        @type grect: L{geosings.core.GeoRect.GeoRect}
        @param grect: 拉框覆盖的地理范围矩形
        @type dcrect: Rect
        @param dcrect: 绘制区域的矩形
        @type mrect: Rect
        @param mrect: 拉框矩形
        @rtype: L{geosings.core.GeoRect.GeoRect}
        @return: 调整大小后需要绘制的地理区域矩形
        """
        mrw = mrect.GetWidth()*1.0
        mrh = mrect.GetHeight()*1.0
        dcw = dcrect.GetWidth()
        dch = dcrect.GetHeight()
        if mrw*1.0/mrh>dcw*1.0/dch:# 按宽调整
            mrh = dch*1.0/dcw*mrw    
        else:
            mrw = dcw*1.0/dch*mrh
        mrmx,mrmy = mrect.GetMiddlePoint()
        x = mrmx-mrw/2 ; y = mrmy-mrh/2
        realw = dcw/mrw*dcw
        realh = dch/mrh*dch
        realx = -(x/dcw*realw)
        realy = -(y/dch*realh)
        realx2 = realx+realw
        realy2 = realy+realh
        realgx,realgy = ScreenPToGeoP(realx,realy,dcrect,grect)
        realgx2,realgy2 = ScreenPToGeoP(realx2,realy2,dcrect,grect)
        return GeoRect(realgx,realgy,realgx2,realgy2)
        
    def __initZoomIn(self,x,y,georect):
        """放大2倍
        @type x,y: number
        @param x,y: 中点位置
        @type georect: L{geosings.core.GeoRect.GeoRect}
        @param georect: 绘制区域所覆盖的空间区域
        @rtype: L{geosings.core.GeoRect.GeoRect}
        @return: 放大两倍后绘制区域所覆盖的空间范围
        """
        hw = georect.GetWidth()/4.0
        hh = georect.GetHeight()/4.0
        return GeoRect(x-hw,y-hh,x+hw,y+hh)

    def __initZoomOut(self,x,y,georect):
        """ 缩小2倍
        @type x,y: number
        @param x,y: 中点位置
        @type georect: L{geosings.core.GeoRect.GeoRect}
        @param georect: 绘制区域所覆盖的空间区域
        @rtype: L{geosings.core.GeoRect.GeoRect}
        @return: 缩小两倍后绘制区域所覆盖的空间范围
        """
        hw = georect.GetWidth()
        hh = georect.GetHeight()
        return GeoRect(x-hw,y-hh,x+hw,y+hh)

    def Zoom(self,zoomtype):
        """控制缩放的总调函数(鼠标位置获取都由内部获取)
        @type zoomtype: ModeKey
        @param zoomtype: 放大还是缩小
        """
        dcrect = self.GetClientRect()
        georect = mainDocument.geoext
        if zoomtype==ModeKey.ZoomInMode:# 放大
            x1,y1 = ScreenPToGeoP(self.tmpxb,self.tmpyb,dcrect,georect)
            x2,y2 = ScreenPToGeoP(self.tmpxe,self.tmpye,dcrect,georect)
            if x1==x2 and y1==y2:
                realgeoext = self.__initZoomIn(x1,y1,georect)
            else:
                mgrect = GeoRect(x1,y1,x2,y2)
                realgeoext = self.__initZoomInRect(mgrect,dcrect.GetWidth(), \
                    dcrect.GetHeight())
        else: # 缩小
            if self.tmpxb==self.tmpxe and self.tmpyb==self.tmpye:
                x1,y1 = ScreenPToGeoP(self.tmpxb,self.tmpyb,dcrect,georect)
                realgeoext = self.__initZoomOut(x1,y1,georect)
            else:
                mrect = GeoRect(self.tmpxb,self.tmpyb,self.tmpxe,self.tmpye)
                realgeoext = self.__initZoomOutRect(georect,dcrect,mrect)
        mainDocument.geoext.ReSet(realgeoext.GetLeft(),realgeoext.GetTop(), \
                realgeoext.GetRight(),realgeoext.GetBottom())
        mainDocument.zoomall = 0
        #self.Refresh()
        self.ReDraw()

    def Aim(self, sth):
        """倏地瞄准某个点
        @type sth: list
        @param sth: 要瞄准的点(或者矩形),矩形四个元素，点是两个元素
        """
        import time
        dc = wx.ClientDC(self)
        dcrect = self.GetClientRect()
        left,right=dcrect.GetLeft(),dcrect.GetRight()
        top,bottom=dcrect.GetTop(),dcrect.GetBottom()
        if len(sth)==2:
            px,py = sth[0],sth[1]
        elif len(sth)==4:
            px,py = sth[0]+sth[2]/2,sth[1]+sth[3]/2
        else:
            return
        point = [px,py]
        if not (left<px<right and top<py<bottom):
            return
        hw = max(px-left,right-px)
        hh = max(py-top,bottom-py)
        hl = max(hw,hh)#计算一个要过渡的矩形范围

        hllen=50 #要移动的线的一半长度

        xmove = hl/20.0 #每次移动多少

        relen = 12#四角框的长度

        dc.SetPen(wx.GREEN_PEN)

        if wx.Platform == "__WXGTK__":
            dc.SetLogicalFunction(wx.XOR)
            pen2 = wx.Pen(wx.WHITE,2,wx.SOLID)
            dc.SetPen(pen2)
            self.__DrawAimLines(dc,point,hl,hllen)
            if len(sth)==4:
                re = self.__ScaleRect(sth, 20-1)
                self.__DrawAimRect(dc,re,0,relen)
            for i in range(20):
                for k in range(20):
                    self.__DrawAimLines(dc,point,hl,hllen)
                if len(sth)==4:
                    re = self.__ScaleRect(sth,20-1-i)
                    self.__DrawAimRect(dc,re,0,relen)
                hl-=xmove
                for k in range(20):
                    self.__DrawAimLines(dc,point,hl,hllen)
                if len(sth)==4 :
                    if i <19:
                        re2 = self.__ScaleRect(sth,20-i-2)
                    else:
                        re2 = self.__ScaleRect(sth,20-i-1)
                    self.__DrawAimRect(dc,re2,0,relen)
            dc.SetLogicalFunction(wx.COPY)
        else:
            dc.SetLogicalFunction(wx.XOR)
            self.__DrawAimLines(dc,point,hl,hllen)
            if len(sth)==4:
                re = self.__ScaleRect(sth, 20-1)
                self.__DrawAimRect(dc,re,0,relen)
            for i in range(20):
                self.__DrawAimLines(dc,point,hl,hllen)
                if len(sth)==4:
                    re = self.__ScaleRect(sth,20-1-i)
                    self.__DrawAimRect(dc,re,0,relen)
                hl-=xmove
                self.__DrawAimLines(dc,point,hl,hllen)
                if len(sth)==4 :
                    if i <19:
                        re2 = self.__ScaleRect(sth,20-i-2)
                    else:
                        re2 = self.__ScaleRect(sth,20-i-1)
                    self.__DrawAimRect(dc,re2,0,relen)
                time.sleep(0.02)
            dc.SetLogicalFunction(wx.COPY)


    def __DrawAimLines(self, dc, point, hl, hllen):
        dc.DrawLine(point[0]-hl-hllen-1,point[1],point[0]-hl+hllen,point[1])
        dc.DrawLine(point[0]+hl-hllen,point[1],point[0]+hl+hllen+1,point[1])
        dc.DrawLine(point[0],point[1]-hl-hllen-1,point[0],point[1]-hl+hllen)
        dc.DrawLine(point[0],point[1]+hl-hllen,point[0],point[1]+hl+hllen+1)

    def __DrawAimRect(self, dc, rect, hl, hllen):
        dc.DrawLine(rect[0],rect[1],rect[0]+hllen,rect[1])
        dc.DrawLine(rect[0],rect[1],rect[0],rect[1]+hllen)
        dc.DrawLine(rect[0]+rect[2],rect[1],rect[0]+rect[2]-hllen,rect[1])
        dc.DrawLine(rect[0]+rect[2],rect[1],rect[0]+rect[2],rect[1]+hllen)
        dc.DrawLine(rect[0],rect[1]+rect[3],rect[0]+hllen,rect[1]+rect[3])
        dc.DrawLine(rect[0],rect[1]+rect[3],rect[0],rect[1]+rect[3]-hllen)
        dc.DrawLine(rect[0]+rect[2],rect[1]+rect[3],rect[0]+rect[2]-hllen,rect[1]+rect[3])
        dc.DrawLine(rect[0]+rect[2],rect[1]+rect[3],rect[0]+rect[2],rect[1]+rect[3]-hllen)

    def __ScaleRect(self, rect, i):
        step = 5
        return [rect[0]-i*(step), rect[1]-i*(step),
                rect[2]+step*i*2, rect[3]+step*i*2]

