# -*- coding: utf-8 -*-
"""
该模块定义主界面的工具栏类
"""

import wx
from geosings.core.system.GssConfDict import GSSCONF,GSSMSGS

from geosings.ui.core.MainImage import GetToolBarImg
from geosings.ui.core.UIConst import *

from Action import *

def InitToolBar(bar,toolconf):
    for tool in toolconf:
        if tool[0]==UI_TYPE_SEPARATOR:
            bar.AddSeparator()
        else:
            tooltype = GetUIWxType(tool[0])
            if tool[0] != UI_TYPE_BUTTON:
                id = tool[1][0]
                bar.ui_feedback[tool[1][1]]=id
            else:
                id = tool[1]
            label = tool[2]
            if tool[3]==TOOLBAR_BITMAP_DEFPATH:
                img = GetToolBarImg(label)
            else:
                img = GetToolBarImg(tool[3],False)
            if tool[4]== None:
                imgex = wx.NullBitmap
            else: imgex = GetToolBarImg(tool[4],False)
            helpstr = GSSCONF[tool[5]]
            bar.AddLabelTool(id,_(label),img,imgex,tooltype,_(helpstr),'')
            #绑定事件
            if len(tool)==7:
                if type(tool[6])==str:
                    msg = GSSMSGS[tool[6]]
                    bar.msgdir[id] = msg
                    bar.BindEvent(id, bar.Call)
                else:#用户定义事件
                    #bar.BindEvent(id, tool[6])
                    bar.foodir[id] = tool[6]
                    bar.BindEvent(id, bar.CallUserFunction)

class MyToolBar(wx.ToolBar):
    """该类定义主界面的工具栏
    """
    def __init__(self,toolconf,frame,hastxt,*args,**kwds):
        #from UISettings import TOOLBAR_BITMAP_SIZE
        from geosings.core.system.GssConfDict import GSSCONF
        TOOLBAR_BITMAP_SIZE = GSSCONF["TOOLBAR_BITMAP_SIZE"]
        # begin wxGlade: MyToolBar.__init__
        if hastxt:
            kwds["style"] = wx.TB_FLAT|wx.TB_DOCKABLE|wx.TB_TEXT
        else:
            kwds["style"] = wx.TB_FLAT|wx.TB_DOCKABLE
        wx.ToolBar.__init__(self, frame, *args, **kwds)
        self.frame = frame
        self.msgdir = {}; self.ui_feedback = {}
        self.foodir = {}
        self.SetToolBitmapSize(TOOLBAR_BITMAP_SIZE)#这句要加在所有添加之前
        InitToolBar(self,toolconf)

        self.__set_properties()
        self.__do_layout()

        #self.Bind(wx.EVT_TOOL, self.OnOpen, id=1)
        #self.Bind(wx.EVT_TOOL, self.OnAddLayer, id=2)
        #self.Bind(wx.EVT_TOOL, self.OnPan, id=3)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyToolBar.__set_properties
        self.Realize()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyToolBar.__do_layout
        pass
        # end wxGlade

    def Call(self,event):
        self.frame.optid = id = event.GetId()
        from PyMainPanel import GetMainPanel
        mainpanel = GetMainPanel()
        msg = self.msgdir[id]
        if msg.startswith(':'):
            mainpanel.ExecMsg(msg)
        else:
            mainpanel.SentOrder(msg)
    
    def CallUserFunction(self,event):
        self.frame.optid = id = event.GetId()
        foo = self.foodir[id]
        #print foo
        if callable(foo):
            foo()

    def OnFoo(self, event): # wxGlade: MyToolBar.<event_handler>
        print "Event handler not implemented!"
        event.Skip()

    def SetMode(self,mode):
        #print 'toolbar:',mode
        #if mode == ModeKey.NoneMode:
        #    self.ToggleTool( ID_TB_NoMode, True)
        #elif mode == ModeKey.PanMode:
        #    self.ToggleTool( ID_TB_Pan, True)
        #elif mode == ModeKey.ZoomInMode:
        #    self.ToggleTool( ID_TB_ZoomIn, True)
        #elif mode == ModeKey.ZoomOutMode:
        #    self.ToggleTool( ID_TB_ZoomOut, True)
        #elif mode == ModeKey.InfoMode:
        #    self.ToggleTool( ID_TB_Info, True)
        self.ToggleTool( self.ui_feedback[mode], True)

    def BindEvent(self,eID,foo):
        self.Bind(wx.EVT_TOOL, foo, id=eID)

    #def BindEvents(self):
    #    """绑定MenuBar和ToolBar的消息
    #    """
    #    self.BindEvent(ID_TB_NoMode, OnMenuMode)
    #    self.BindEvent(ID_TB_Pan, OnMenuMode)
    #    self.BindEvent(ID_TB_ZoomIn, OnMenuMode)
    #    self.BindEvent(ID_TB_ZoomOut, OnMenuMode)
    #    self.BindEvent(ID_TB_Info, OnMenuMode)
    #    self.BindEvent(ID_TB_Open, OnMenuMsg)
    #    self.BindEvent(ID_TB_Save, OnMenuMsg)
    #    self.BindEvent(ID_TB_AddLayer, OnMenuMsg)

# end of class MyToolBar

mainToolbar = None

def CreateMainToolBar(mainframe,toolconf):
    """创建主面板
    """
    global mainToolbar
    from UISettings import *
    mainToolbar = MyToolBar(toolconf,mainframe,GSSCONF["HAS_TOOLBAR_TEXT"])
    #mainToolbar.BindEvents()
    return mainToolbar

def GetMainToolBar():
    """获取主面板
    """
    global mainToolbar
    return mainToolbar
