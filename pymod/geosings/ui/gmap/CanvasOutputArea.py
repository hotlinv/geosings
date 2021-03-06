﻿# -*- coding: utf-8 -*-
"""
该模块定义在画布上的输出区域
"""

import wx
#from UISettings import *
from geosings.core.system.GLog import *
from geosings.core.system.GssConfDict import GSSCONF

class CanvasOutputArea:
    """画布输出区域控件
    """
    def __init__(self):
        """构造函数
        """
        pass

    def Init(self,parent):
        """初始化控件
        @type parent: ctrl
        @param parent: 该控件所属的父控件
        """
        self.parent = parent
        if GSSCONF["HAS_MODE_LABEL"]:
            self.label_1 = wx.StaticText(self.parent, -1, "lab1")
        self.label_msgs = []
        for i in range(GSSCONF["CANV_OP_MSG_NUM"]):
            self.label_msgs.append(wx.StaticText(self.parent,-1,"."))
        #self.label_2 = wx.StaticText(self.parent, -1, "lab2")
        #self.label_3 = wx.StaticText(self.parent, -1, "lab3")
        bindLogCaller(self)
        bindInfoCaller(self)
        bindDebugCaller(self)
        bindErrCaller(self)

    def InitLayout(self):
        """初始化控件的排列位置
        """
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(3, 3, 0, 0)
        if GSSCONF["HAS_MODE_LABEL"]:
            self.label_1.SetForegroundColour(wx.RED)
            sizer_1.Add(self.label_1, 1, wx.ADJUST_MINSIZE|wx.ALIGN_RIGHT, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        for i in range(GSSCONF["CANV_OP_MSG_NUM"]):
            sizer_1.Add(self.label_msgs[i], 0, wx.ADJUST_MINSIZE, 0)
        #sizer_1.Add(self.label_2, 0, wx.ADJUST_MINSIZE, 0)
        #sizer_1.Add(self.label_3, 0, wx.ADJUST_MINSIZE, 0)
        self.parent.SetSizer(sizer_1)
        sizer_1.Fit(self.parent)
        sizer_1.SetSizeHints(self.parent)
        self.mainsizer = sizer_1
        self.parent.SetAutoLayout(True)

    def SetMode(self,mode):
        """设置模式的选择
        @type mode: str
        @param mode: 要显示的模式类型名
        """
        if GSSCONF["HAS_MODE_LABEL"]:
            self.label_1.SetLabel(mode)
        else:
            pass


    def ShowMsg(self,msg):
        """显示信息
        @type msg: str
        @param msg: 要显示的信息
        """
        CANV_OP_MSG_NUM = GSSCONF["CANV_OP_MSG_NUM"]
        self.__MsgUp()
        if CANV_OP_MSG_NUM > 0:
            self.label_msgs[CANV_OP_MSG_NUM-1].SetForegroundColour(GSSCONF["INFO_COLOR"])
            self.label_msgs[CANV_OP_MSG_NUM-1].SetLabel(msg)


    def ShowError(self,msg):
        """显示错误
        @type msg: str
        @param msg: 要显示的错误信息
        """
        CANV_OP_MSG_NUM = GSSCONF["CANV_OP_MSG_NUM"]
        self.__MsgUp()
        if CANV_OP_MSG_NUM > 0:
            #print 'err showing'
            self.label_msgs[CANV_OP_MSG_NUM-1].SetForegroundColour(GSSCONF["ERR_COLOR"])
            self.label_msgs[CANV_OP_MSG_NUM-1].SetLabel(msg)

    def __MsgUp(self):
        """信息向上滚动
        """
        CANV_OP_MSG_NUM = GSSCONF["CANV_OP_MSG_NUM"]
        if CANV_OP_MSG_NUM == 0:
            return
        if CANV_OP_MSG_NUM>len(self.label_msgs):
            #万一数量不够，就要扩展消息数组
            extmsgs = [wx.StaticText(self.parent,-1,".") for i in \
                    range(CANV_OP_MSG_NUM-len(self.label_msgs)) ]
            for txt in extmsgs:
                self.mainsizer.Add(txt, 0, wx.ADJUST_MINSIZE, 0)
            self.label_msgs.extend(extmsgs)
            self.mainsizer.Layout()

        for i in range(CANV_OP_MSG_NUM-1):
            self.label_msgs[i].SetForegroundColour(
                        self.label_msgs[i+1].GetForegroundColour())
            #print i-1,self.label_msgs[i+1].GetLabel()
            self.label_msgs[i].SetLabel(
                        self.label_msgs[i+1].GetLabel())

    def log(self,msg):
        CANV_OP_MSG_NUM = GSSCONF["CANV_OP_MSG_NUM"]
        self.__MsgUp()
        if CANV_OP_MSG_NUM > 0:
            self.label_msgs[CANV_OP_MSG_NUM-1].SetForegroundColour(GSSCONF["LOG_COLOR"])
            self.label_msgs[CANV_OP_MSG_NUM-1].SetLabel(msg)
    def info(self,msg):
        self.ShowMsg(msg)
    def debug(self,msg):
        CANV_OP_MSG_NUM = GSSCONF["CANV_OP_MSG_NUM"]
        self.__MsgUp()
        if CANV_OP_MSG_NUM > 0:
            self.label_msgs[CANV_OP_MSG_NUM-1].SetForegroundColour(GSSCONF["DEBUG_COLOR"])
            self.label_msgs[CANV_OP_MSG_NUM-1].SetLabel(msg)
    def err(self,msg):
        self.ShowError(msg)

