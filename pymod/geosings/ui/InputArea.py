# -*- coding: utf-8 -*-
"""
该模块定义输入控件
"""
import wx
from geosings.ui.core.wxKeyParser import *
from geosings.core.system.FillLine import fillline
from geosings.core.system.EncodeTran import utf82locale

class InputArea(wx.TextCtrl):
    """输入区域控件
    """
    def __init__(self, parent, id=-1, value="",
            pos=wx.Point(0,0), size=wx.Size(-1,-1), style=0,
            validator=wx.Validator(), name="TextInput"):
        """初始化控件
        @type parent: wxCtrl
        @param parent: 父控件
        @type id: int
        @param id: 控件的id
        @type value: str
        @param value: 控件上显示的初始内容
        @type pos: wxPoint
        @param pos: 控件初始位置
        @type size: wxSize
        @param size: 控件初始大小
        @type style: wxStyle
        @param style: 类型
        @type validator: wxValidator
        @param validator: 认证
        @type name: str
        @param name: 控件名字
        """
        wx.TextCtrl.__init__(self,parent,id,value,pos,size,
                style|wx.TE_PROCESS_ENTER ,validator,name)
        self.parent = parent
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.ordlist = [] #放历史命令
        self.at = 0

    def OnChar(self, evt):
        """键盘响应函数
        @type evt: wxEvent
        @param evt: 键盘响应事件
        """
        kp = KeyParser(evt)
        keycode = kp.keycode
        #print keycode
        if keycode==27:# escape
            self.parent.OutputMsg('')
            self.parent.EnableInput(False)
        elif keycode==13:# enter
            self.ordlist.append(self.GetValue())
            self.at = len(self.ordlist)
            msg = utf82locale(self.GetValue())
            self.parent.ExecMsg(msg)
            self.parent.EnableInput(False)
        elif keycode == 8:# back
            if len(self.GetValue())==1:
                self.parent.EnableInput(False)
            else:evt.Skip(True)
        elif keycode == 9:# tab
            self.SetValue(fillline.GetLine(self.GetValue()))
            self.SetInsertionPointEnd()
        elif keycode == 315:# up
            if self.at>=1:
                self.at-=1
            self.SetValue(self.ordlist[self.at])
            self.SetInsertionPointEnd()
        elif keycode == 317:# down
            if self.at+1<len(self.ordlist):
                self.at+=1
            self.SetValue(self.ordlist[self.at])
            self.SetInsertionPointEnd()
        else:evt.Skip(True)
