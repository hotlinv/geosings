# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.6.29; version:1; 创建
"""
该模块定义栅格影像分割工具操作界面
"""

from geosings.ui.commondlg.ToolCtrlBasePanel import *
from geosings.tools.RasterOperator import RasterSplitter
import geosings.core.system.UseGetText

import wx,os

class RasterSplitterUI(ToolCtrlBasePanel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        ToolCtrlBasePanel.__init__(self, *args, **kwds)
        #self.itype = "None"#不需要输入
        #self.otype = "None"#不需要输出
        sizer = wx.FlexGridSizer(cols=2,vgap=1,hgap=1)
        bwtxt = wx.StaticText(self, -1, _("block width")+":")
        self.bwed = wx.TextCtrl(self, -1, "128")
        sizer.Add(bwtxt)
        sizer.Add(self.bwed)
        bhtxt = wx.StaticText(self, -1, _("block height")+":")
        self.bhed = wx.TextCtrl(self, -1, "128")
        sizer.Add(bhtxt)
        sizer.Add(self.bhed)
        self.SetSizer(sizer)
        self.Layout()
        
    def RunTool(self, layers, outSource, outName):
        path = os.path.join(outSource,outName)
        if len(layers)==1:
            bh = int(self.bhed.GetValue())
            bw = int(self.bwed.GetValue())
            RasterSplitter(layers[0]).Split(path,bw,bh)
        else:
            PopMessage(E("layers count must be 1"))
