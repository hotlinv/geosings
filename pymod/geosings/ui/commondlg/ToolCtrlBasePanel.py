# -*- coding: utf-8 -*-

"""
该模块定义工具UI的基本基类
"""

import wx

def PopMessage(err,parent=None):
    """弹出信息对话框
    """
    msgdlg = wx.MessageDialog(parent,err)
    msgdlg.ShowModal()

class ToolCtrlBasePanel(wx.Panel):
    """
    工具UI的基本面板基类
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.itype = "layer"#,layername,string

    def RunTool(self, layers, outSource, outName):
        """每个子类都需要继承的运行方法（纯虚类型方法）
        """
        pass
