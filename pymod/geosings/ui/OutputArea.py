# -*- coding: utf-8 -*-
"""
该模块定义输出(状态栏)控件
"""

import wx
from geosings.ui.gmap.GOperHandler import OperHandler
from geosings.core.system import ScreenPToGeoP


class OutputArea(wx.Panel):
    """输出区域控件（有可能是状态栏）
    """
    class PointWhereHandler(OperHandler):
        def __init__(self,ctrl):
            OperHandler.__init__(self, ctrl)
        def SetCanvas(self, canvas):
            self.canvas = canvas
        def OnMotion(self, evt):
            x,y = self.canvas.GetPointCoor(evt.GetX(),evt.GetY())
            self.ctrl.PrintMouse(x,y)
    def __init__(self,parent):
        """初始化控件
        @type parent: wxCtrl
        @param parent: 父控件
        """
        wx.Panel.__init__(self,parent,-1)
        self.parent = parent
        self.MsgArea = wx.StaticText(self, -1, "")
        self.ModeArea = wx.StaticText(self,-1,"mode",size=wx.Size(130,-1),
                style=wx.ALIGN_LEFT)
        #self.MouseArea = wx.StaticText(self, -1,
        #        "mouse",size=wx.Size(250,-1),
        #        style=wx.ALIGN_RIGHT)
        self.MouseArea = wx.StaticText(self, -1 , 'mouse')
        #self.ModeArea.SetBackgroundColour('Yellow')

        self.mouseHandler = OutputArea.PointWhereHandler(self)
        
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        """设置控件属性
        """
        # begin wxGlade: MyPanel.__set_properties
        pass
        self.SetBackgroundColour(wx.BLACK)
        self.MsgArea.SetForegroundColour(wx.WHITE)
        self.ModeArea.SetForegroundColour(wx.WHITE)
        self.MouseArea.SetForegroundColour(wx.WHITE)

    def __do_layout(self):
        """设置控件布局
        """
        # begin wxGlade: MyPanel.__do_layout
        if 'wxMSW' in wx.PlatformInfo:
            sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_4 = wx.BoxSizer(wx.VERTICAL)
            sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)
            sizer_4.Add(self.MsgArea, 1, wx.EXPAND, 0)
            sizer_3 = wx.BoxSizer(wx.VERTICAL)
            sizer_1.Add(sizer_3, 0, wx.FIXED_MINSIZE,0)
            sizer_3.Add(self.ModeArea, 0, wx.ALIGN_LEFT, 0)
            self.sizer_2 = wx.BoxSizer(wx.VERTICAL)
            sizer_1.Add(self.sizer_2, 0, wx.EXPAND,0)
            self.sizer_2.Add(self.MouseArea, 0, wx.ALIGN_RIGHT, 0)
        elif 'wxGTK' in wx.PlatformInfo:
            sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_1.Add(self.MsgArea,1,wx.EXPAND, 0)
            sizer_1.Add(self.ModeArea, 0, wx.ADJUST_MINSIZE, 0)
            sizer_1.Add(self.MouseArea, 0, wx.ALIGN_RIGHT, 0)
        self.mainsizer = sizer_1
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        self.mainsizer.Layout()
        self.Layout()
        self.parent.Layout()
        #sizer_1.Fit(self)
        #sizer_1.SetSizeHints(self)
        # end wxGlade

    def SetMsg(self,msg):
        """输出消息
        @type msg: str
        @param msg: 输出消息
        """
        #print msg
        self.MsgArea.SetLabel(msg)
        #if len(msg)>20:
            #self.Layout()
            #self.parent.Layout()
        self.mainsizer.Layout()

    def PrintMouse(self,x,y):
        """打印鼠标
        @type x,y: float
        @param x,y: 鼠标位置
        """
        mousestr = 'X:%lf/Y:%lf' % (x,y)
        self.MouseArea.SetLabel(mousestr)
        if 'wxGTK' in wx.PlatformInfo:
            #self.Layout()
	    pass
            #self.sizer_2.Layout()
        elif 'wxMSW' in wx.PlatformInfo: 
            self.sizer_2.Layout()
            pass
        self.mainsizer.Layout()
        #self.parent.Layout()

    def PrintMode(self,modename):
        """打印模式
        @type modename: str
        @param modename: 模式名
        """
        #self.ModeArea.SetValue(modename)
        self.ModeArea.SetLabel(modename)
        #self.Layout()
        self.mainsizer.Layout()
        #self.parent.Layout()
