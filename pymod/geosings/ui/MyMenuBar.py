# -*- coding: utf-8 -*-
"""
该模块定义主界面的菜单类
"""

import wx

import geosings.core.system.UseGetText
from geosings.core.system.GssConfDict import GSSCONF,GSSMSGS

from geosings.ui.core.UIConst import *
from Action import *


def InitMenuBar(mainbar,bar,frame,menuconf):
    for menu in menuconf:
        if menu[0]==UI_TYPE_SEPARATOR:
            bar.AppendSeparator()
        elif menu[0]==UI_TYPE_POPUP:
            submenu=wx.Menu()
            InitMenuBar(mainbar,submenu,frame,menu[2])
            bar.Append(submenu,_(menu[1]))
        else:
            tooltype = GetUIWxType(menu[0])
            if menu[0] != UI_TYPE_BUTTON:
                id = menu[1][0]
                mainbar.ui_feedback[menu[1][1]]=id
            else:
                id = menu[1]
            label = menu[2]
            description = menu[3]
            menuitem = wx.MenuItem(bar,id,_(label),description,tooltype)
            bar.AppendItem(menuitem)
            #绑定事件
            if len(menu)==5:
                if type(menu[4])==str:
                    msg = GSSMSGS[menu[4]]
                    mainbar.msgdir[id] = msg
                    mainbar.BindEvent(frame, id, mainbar.Call)
                else:#用户定义事件
                    mainbar.foodir[id] = menu[4]
                    mainbar.BindEvent(frame, id, mainbar.CallUserFunction)


class MyMenuBar(wx.MenuBar):
    """该类是主界面菜单
    """
    def __init__(self, mainframe, menuconf, *args, **kwds):
        # begin wxGlade: MyMenuBar.__init__
        wx.MenuBar.__init__(self, *args, **kwds)
        self.frame = mainframe
        self.msgdir = {}; self.ui_feedback = {}
        self.foodir = {}
        InitMenuBar(self,self,mainframe,menuconf)

        self.__set_properties()
        self.__do_layout()

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyMenuBar.__set_properties
        pass
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyMenuBar.__do_layout
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

    def SetMode(self,mode):
        #print 'menu:',mode
        #if mode == ModeKey.NoneMode:
        #    self.FindItemById(ID_MB_NoMode).Check(True)
        #elif mode == ModeKey.PanMode:
        #    self.FindItemById(ID_MB_Pan).Check(True)
        #elif mode == ModeKey.ZoomInMode:
        #    self.FindItemById(ID_MB_ZoomIn).Check(True)
        #elif mode == ModeKey.ZoomOutMode:
        #    self.FindItemById(ID_MB_ZoomOut).Check(True)
        #elif mode == ModeKey.InfoMode:
        #    self.FindItemById(ID_MB_Info).Check(True)
        self.FindItemById(self.ui_feedback[mode]).Check(True)

    def BindEvent(self,frame,eID,foo):
        frame.Bind(wx.EVT_MENU, foo, id=eID)
        #frame.Bind(wx.EVT_MENU, foo, id=self.FindItemById(eID))

    def OnFoo(self, event): # wxGlade: MyMenuBar.<event_handler>
        print "Event handler not implemented!"
        event.Skip()

    #def BindEvents(self,frame):
    #    """绑定MenuBar和ToolBar的消息
    #    @type frame: wxFrame
    #    @param frame: 要绑定消息的框架。注意，这里消息只能在框架中绑定，在Menu中绑定无效。
    #    """
    #    self.BindEvent(frame, ID_MB_NoMode, OnMenuMode)
    #    self.BindEvent(frame, ID_MB_Pan, OnMenuMode)
    #    self.BindEvent(frame, ID_MB_ZoomIn, OnMenuMode)
    #    self.BindEvent(frame, ID_MB_ZoomOut, OnMenuMode)
    #    self.BindEvent(frame, ID_MB_Info, OnMenuMode)
    #    self.BindEvent(frame, ID_MB_Exit, OnMenuMsg)
    #    self.BindEvent(frame, ID_MB_Open, OnMenuMsg)
    #    self.BindEvent(frame, ID_MB_AddLayer, OnMenuMsg)

# end of class MyMenuBar

mainMenubar = None

def CreateMainMenuBar(mainframe, menuconf):
    """创建主面板
    """
    global mainMenubar
    mainMenubar = MyMenuBar(mainframe, menuconf)
    return mainMenubar

def GetMainMenuBar():
    """获取主面板
    """
    global mainMenubar
    return mainMenubar
