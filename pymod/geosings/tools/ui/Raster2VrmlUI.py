# -*- coding: utf-8 -*-

"""
该模块定义raster2vrml工具的UI定义
"""
from geosings.ui.commondlg.ToolCtrlBasePanel import *
from geosings.tools.raster2vrml import Raster2Vrml
import geosings.core.system.UseGetText

import wx
class Raster2VrmlUI(ToolCtrlBasePanel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        ToolCtrlBasePanel.__init__(self, *args, **kwds)
        self.check = wx.CheckBox(self, -1, _("output the image mask")+"?")

    def RunTool(self, layers, outSource, outName):
        if len(layers)==1:
            layer = layers[0]
            Raster2Vrml().Convert(layer, outSource, outName, convimg=self.check.IsChecked())
        else:
            PopMessage(E("layers count must be 1"))
