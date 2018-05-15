# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.7.2; version:1; 创建
"""
该模块定义栅格缩放工具界面
"""

from geosings.ui.commondlg.ToolCtrlBasePanel import *
from geosings.tools.RasterOperator import ResizeRaster
import geosings.core.system.UseGetText

import wx,os

class RasterResizerUI(ToolCtrlBasePanel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        ToolCtrlBasePanel.__init__(self, *args, **kwds)
        #self.itype = "None"#不需要输入
        #self.otype = "None"#不需要输出
        sizer = wx.FlexGridSizer(cols=2,vgap=1,hgap=1)
        scaletxt = wx.StaticText(self, -1, _("scale")+":")
        self.scaleed = wx.TextCtrl(self, -1, "1.0/2")
        sizer.Add(scaletxt)
        sizer.Add(self.scaleed)
        self.SetSizer(sizer)
        self.Layout()
        
    def RunTool(self, layers, outSource, outName):
        path = os.path.join(outSource,outName)
        if len(layers)==1:
            raster = layers[0].DataSet()
            comm = "scale = %s" % self.scaleed.GetValue()
            exec comm
            ResizeRaster(raster,scale,path)
        else:
            PopMessage(E("layers count must be 1"))
