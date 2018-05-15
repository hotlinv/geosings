#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
屏幕输出区域

 - writer:linux_23; create: Sun Jun  1 18:39:51 2008 ; version:1; 创建
"""


import wx
from geosings.core.system.GLog import *
from geosings.core.system.GssConfDict import GSSCONF
import geosings.core.system.UseGetText
from geosings.ui.gmap.GOperHandler import OperHandler

class wxLogHandler(logging.Handler,OperHandler):
    """
    界面的log操作Handler
    """
    def __init__(self, uictrl):
        logging.Handler.__init__(self)
        OperHandler.__init__(self,uictrl)
        self.ui = uictrl
        self.levelcolor = [
            wx.NamedColour('GRAY'),#wx.TextAttr("GRAY", wx.NullColour),#DEBUG
            wx.NamedColour('BLACK'),#wx.TextAttr("BLACK", wx.NullColour),#INFO
            wx.NamedColour('ORANGE'),#wx.TextAttr("ORANGE", wx.NullColour),#WARNING
            wx.NamedColour('RED'),#wx.TextAttr("RED", wx.NullColour),#ERROR
            wx.NamedColour('PINK'),#wx.TextAttr("PINK", wx.NullColour),#CRITICAL
            wx.NamedColour('BLUE'),#wx.TextAttr("BLUE", wx.NullColour),#ORDER
        ]
        self.drawer = uictrl.handler
        self.bgbmps = []
        self.loginfo = []
    def flush(self):
        pass
    
    def PrintText(self, bgbmp, text, pos, color=wx.BLACK):
        bg_colour = wx.Colour(57, 115, 57)  # matches the bg image
        font = self.ui.parent.GetFont()
        textExtent = self.ui.parent.GetFullTextExtent(text, font)

        # create a bitmap the same size as our text
        bmp = wx.EmptyBitmap(textExtent[0], textExtent[1])

        # 'draw' the text onto the bitmap
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(bg_colour, wx.SOLID))
        dc.Clear()
        dc.SetTextForeground(color)
        dc.SetFont(font)
        dc.DrawText(text, 0, 0)
        dc.SelectObject(wx.NullBitmap)
        mask = wx.Mask(bmp, bg_colour)
        bmp.SetMask(mask)
        
        memDC = wx.MemoryDC()

        bc = wx.BufferedDC(None, self.ui.parent.buffer)
        if bgbmp:
            memDC.SelectObject(bgbmp)
            bc.Blit(pos[0],pos[1], bgbmp.GetWidth(), bgbmp.GetHeight(),
                    memDC, 0, 0, wx.COPY, True)
        tbgbmp = wx.EmptyBitmap(textExtent[0], textExtent[1])
        memDC.SelectObject(tbgbmp)
        memDC.Blit(0, 0, bmp.GetWidth(), bmp.GetHeight(),
                bc, pos[0], pos[1], wx.COPY, True)
        #self.bgpos = pos
        memDC.SelectObject(bmp)
        bc.Blit(pos[0], pos[1], bmp.GetWidth(), bmp.GetHeight(),
                memDC, 0, 0, wx.COPY, True)
        self.ui.parent.Refresh()
        return tbgbmp
    
    def OnEDraw(self, gc):
        if isinstance(gc, wx.BufferedDC):
            self.bgbmps = [None for i in range(len(self.bgbmps))]

        rect = self.ui.parent.GetClientRect()
        font = self.ui.parent.GetFont()
        bi = len(self.loginfo)
        i = 0
        # Make a shape from some text
        for logi in self.loginfo:
            txt, color = logi[0], logi[1]
            textExtent = self.ui.parent.GetFullTextExtent(txt, font)
            self.bgbmps[i] = self.PrintText(self.bgbmps[i], txt, (0, rect.GetHeight()-textExtent[1]*bi),color)
            bi-=1
            i+=1

    def ShowMsg(self,msg, color):
        """显示信息
        @type msg: str
        @param msg: 要显示的信息
        """
        CANV_OP_MSG_NUM = GSSCONF["CANV_OP_MSG_NUM"]
        self.loginfo.append([msg, color])

        rect = self.ui.parent.GetClientRect()
        font = self.ui.parent.GetFont()
        textExtent = self.ui.parent.GetFullTextExtent(msg, font)
        if len(self.loginfo)>CANV_OP_MSG_NUM:
            self.loginfo.pop(0)
        #else:
        #    self.bgpos = (0, rect.GetHeight()-textExtent[1]*len(self.loginfo))

        if CANV_OP_MSG_NUM > 0:
            bi = len(self.loginfo)
            if len(self.bgbmps)<len(self.loginfo):
                self.bgbmps.insert(0,None)
            i = 0
            for logi in self.loginfo:
                txt, color = logi[0], logi[1]
                self.bgbmps[i] = self.PrintText(self.bgbmps[i], txt, (0, rect.GetHeight()-textExtent[1]*bi),color)
                bi-=1
                i+=1
                #self.ui.label_msgs[CANV_OP_MSG_NUM-1].SetForegroundColour(color)
                #self.ui.label_msgs[CANV_OP_MSG_NUM-1].SetLabel(msg)

    def emit(self, record):
        """
        处理一个记录
        """
        try:
            msg = self.format(record)
            fs = "%s\n"
            i = 1
            levelcolor = self.levelcolor[-1]
            for color in self.levelcolor:
                if record.levelno<10*(i+1):
                    levelcolor = color
                    break
                i+=1
            #self.ui.SetDefaultStyle(levelcolor)
            #self.ui.AppendText(fs % any2utf8(msg))

            self.ShowMsg(fs % any2utf8(msg), levelcolor)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

class DrawHandler(OperHandler):
    def __init__(self, ctrl):
        OperHandler.__init__(self,ctrl)
        self.bgbmp = None
        self.bgpos = (0,0)

    def PrintText(self, text, pos, color=wx.BLACK):
        bg_colour = wx.Colour(57, 115, 57)  # matches the bg image
        font = self.ctrl.parent.GetFont()
        textExtent = self.ctrl.parent.GetFullTextExtent(text, font)

        # create a bitmap the same size as our text
        bmp = wx.EmptyBitmap(textExtent[0], textExtent[1])

        # 'draw' the text onto the bitmap
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(bg_colour, wx.SOLID))
        dc.Clear()
        dc.SetTextForeground(color)
        dc.SetFont(font)
        dc.DrawText(text, 0, 0)
        dc.SelectObject(wx.NullBitmap)
        mask = wx.Mask(bmp, bg_colour)
        bmp.SetMask(mask)
        
        memDC = wx.MemoryDC()

        bc = wx.BufferedDC(None, self.ctrl.parent.buffer)
        if self.bgbmp:
            memDC.SelectObject(self.bgbmp)
            bc.Blit(self.bgpos[0],self.bgpos[1], self.bgbmp.GetWidth(), self.bgbmp.GetHeight(),
                    memDC, 0, 0, wx.COPY, True)
        self.bgbmp = wx.EmptyBitmap(textExtent[0], textExtent[1])
        memDC.SelectObject(self.bgbmp)
        memDC.Blit(0, 0, bmp.GetWidth(), bmp.GetHeight(),
                bc, pos[0], pos[1], wx.COPY, True)
        self.bgpos = pos
        memDC.SelectObject(bmp)
        bc.Blit(pos[0], pos[1], bmp.GetWidth(), bmp.GetHeight(),
                memDC, 0, 0, wx.COPY, True)
        self.ctrl.parent.Refresh()

    def OnEDraw(self, gc):
        if isinstance(gc, wx.BufferedDC):
            self.bgbmp = None

        # Make a shape from some text
        text = self.ctrl.modename
        font = self.ctrl.parent.GetFont()
        textExtent = self.ctrl.parent.GetFullTextExtent(text, font)
        rect = self.ctrl.parent.GetClientRect()
        pos = (rect.GetWidth()-textExtent[0], 0)

        self.PrintText(text, pos, wx.RED)
        

class MapCanvasOutputArea:
    """画布输出区域控件
    """
    def __init__(self):
        """构造函数
        """
        pass

    def RegCtrl(self,parent):
        """初始化控件
        @type parent: ctrl
        @param parent: 该控件所属的父控件
        """
        self.parent = parent
        self.handler = DrawHandler(self)
        self.parent.RegHandler(self.handler)
        if GSSCONF["HAS_MODE_LABEL"]:
            self.modename = ""
        #self.label_msgs = []
        #for i in range(GSSCONF["CANV_OP_MSG_NUM"]):
        #    labelmsg = wx.StaticText(self.parent,-1,".")
        #    labelmsg.SetWindowStyle(wx.TRANSPARENT_WINDOW)
        #    self.label_msgs.append(labelmsg)
        self.logh = wxLogHandler(self)
        register_log_handler(self.logh, logging.DEBUG)
        self.parent.RegHandler(self.logh)

    def InitLayout(self):
        """初始化控件的排列位置
        """
        pass

    def SetMode(self,mode):
        """设置模式的选择
        @type mode: str
        @param mode: 要显示的模式类型名
        """
        if GSSCONF["HAS_MODE_LABEL"]:
            self.modename = _(mode)
            self.handler.OnEDraw(wx.ClientDC(self.parent))
        else:
            pass

