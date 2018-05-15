﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.3.5.1 on Wed Aug 30 10:09:45 2006
"""该模块定义gsstools输入输出对话框通用的模板

输入一个图层(文件)，输出一个新的图层(文件)的对话框


!!!!!!!!!!!!!!废弃，以ToolDlgTemplate体系代替!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

import wx
from SelPathDlg import SelPathDlg

class IOCtrl:
    """对话框输入输出的保存类
    """
    def __init__(self):
        """初始化
        """
        self.istr = ""
        self.ostr = ""

    def __str__(self):
        """打印输入输出的内置函数, 可以用str()函数调用的
        """
        return 'input: %s , output: %s ' % (self.istr,self.ostr)

class MyDialog(wx.Dialog):
    """输入输出对话框的主对话框
    """
    def __init__(self, *args, **kwds):
        """初始化对话框
        """
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU#|wx.FRAME_TOOL_WINDOW
        wx.Dialog.__init__(self, *args, **kwds)
        self.ctrl = IOCtrl()
        self.panel_7 = wx.Panel(self, -1)
        self.panel_8 = wx.Panel(self, -1)
        self.label_1 = wx.StaticText(self.panel_8, -1, u"输入")
        self.text_ctrl_2 = wx.TextCtrl(self.panel_8, -1, "")
        self.button_8 = wx.Button(self.panel_8, -1, "...")
        self.label_2 = wx.StaticText(self.panel_8, -1, u"输出")
        self.text_ctrl_3 = wx.TextCtrl(self.panel_8, -1, "")
        self.button_9 = wx.Button(self.panel_8, -1, "...")
        self.panel_9 = wx.Panel(self.panel_8, -1)
        self.static_line_3 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        self.butOK = wx.Button(self.panel_7, wx.ID_OK, "OK")
        self.butCANCEL = wx.Button(self.panel_7, wx.ID_CANCEL, "Cancel")

        self.__set_properties()
        self.__do_layout()
        wx.EVT_BUTTON( self, wx.ID_OK, self.OnOK )
        wx.EVT_BUTTON( self, wx.ID_CANCEL, self.OnCancel )
        self.button_8.Bind(wx.EVT_BUTTON, self.SelInput )
        self.button_9.Bind(wx.EVT_BUTTON, self.SelOutput )
        # end wxGlade

    def SelInput(self,evt):
        """设置输入的按钮的响应
        @type evt: wxEvent
        @param evt: 按钮事件
        """
        pathdlg = SelPathDlg(self)
        pathdlg.ShowModal()
        self.text_ctrl_2.SetValue(pathdlg.GetPath())

    def SelOutput(self,evt):
        """设置输出的按钮的响应
        @type evt: wxEvent
        @param evt: 按钮事件
        """
        pathdlg = SelPathDlg(self)
        pathdlg.ShowModal()
        self.text_ctrl_3.SetValue(pathdlg.GetPath())

    def OnOK(self,evt):
        """ok按钮的响应
        @type evt: wxEvent
        @param evt: OK按钮事件
        """
        self.ctrl.ostr = self.text_ctrl_3.GetValue()
        self.ctrl.istr = self.text_ctrl_2.GetValue()
        if self.Validate():
            self.EndModal(wx.ID_OK)
            self.Destroy()


    def OnCancel(self,evt):
        """Cancel按钮的响应
        @type evt: wxEvent
        @param evt: Cancel按钮事件
        """
#        self.ctrl.ostr = self.text_ctrl_3.GetValue()
#        self.ctrl.istr = self.text_ctrl_2.GetValue()
        self.EndModal(wx.ID_CANCEL)
        self.Destroy()

    def __set_properties(self):
        """设置属性
        """
        # begin wxGlade: MyFrame.__set_properties
        #self.SetTitle("frame_1")
        self.SetSize((595, 167))
        self.button_8.SetSize((30, 24))
        self.button_8.SetDefault()
        self.button_9.SetSize((30, 24))
        self.button_9.SetDefault()
        self.butOK.SetDefault()
        self.butCANCEL.SetDefault()
        # end wxGlade

    def __do_layout(self):
        """设置对话框布局
        """
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8.Add((20, 10), 0, wx.FIXED_MINSIZE, 0)
        sizer_9.Add(self.label_1, 0, wx.FIXED_MINSIZE, 0)
        sizer_9.Add(self.text_ctrl_2, 1, wx.FIXED_MINSIZE, 0)
        sizer_9.Add(self.button_8, 0, wx.SHAPED|wx.ADJUST_MINSIZE, 0)
        sizer_8.Add(sizer_9, 0, wx.EXPAND, 0)
        sizer_8.Add((5, 20), 0, wx.FIXED_MINSIZE, 0)
        sizer_10.Add(self.label_2, 0, wx.FIXED_MINSIZE, 0)
        sizer_10.Add(self.text_ctrl_3, 1, wx.FIXED_MINSIZE, 0)
        sizer_10.Add(self.button_9, 0, wx.SHAPED|wx.ADJUST_MINSIZE, 0)
        sizer_8.Add(sizer_10, 0, wx.EXPAND, 0)
        sizer_8.Add(self.panel_9, 1, wx.EXPAND, 0)
        self.panel_8.SetAutoLayout(True)
        self.panel_8.SetSizer(sizer_8)
        sizer_8.Fit(self.panel_8)
        sizer_8.SetSizeHints(self.panel_8)
        sizer_5.Add(self.panel_8, 1, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_3, 0, wx.EXPAND, 0)
        sizer_11.Add((20, 5), 0, wx.FIXED_MINSIZE, 0)
        sizer_11.Add(self.butOK, 0, wx.FIXED_MINSIZE, 5)
        sizer_11.Add(self.butCANCEL, 0, wx.FIXED_MINSIZE, 5)
        self.panel_7.SetAutoLayout(True)
        self.panel_7.SetSizer(sizer_11)
        sizer_11.Fit(self.panel_7)
        sizer_11.SetSizeHints(self.panel_7)
        sizer_5.Add(self.panel_7, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        self.Layout()
        #self.Centre()
        # end wxGlade

    def GetIO(self):
        """获取输入和输出的路径
        @rtype: L{geosings.tools.IOCtrl}
        @return: 输入输出的存储对象
        """
        return self.ctrl

# end of class MyFrame
def runUI(title):
    """运行对话框UI
    @type title: str
    @param title: 对话框名称
    """
    dlg_1 = MyDialog(None,-1,title)
    ret = dlg_1.ShowModal()
    #print 'exit','return:',ret
    if ret == wx.ID_OK:
        ioc = dlg_1.GetIO()
        return [ioc.istr,ioc.ostr]
    else:
        return ["",""]

def runApp():
    """测试
    """
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyDialog(None, -1, "")
    app.SetTopWindow(frame_1)
    ret = frame_1.ShowModal()
    #print ret,frame_1.GetIO()
    app.MainLoop()

if __name__ == "__main__":
    runApp()
