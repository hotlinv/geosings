# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.6.24; version:1; 创建
"""
该模块定义Ogr2ogr4intoPG工具的UI定义
"""
from geosings.ui.commondlg.ToolCtrlBasePanel import *
from geosings.tools.Ogr2ogr import Ogr2ogr4intoPG
from geosings.core.system.EncodeTran import utf82locale

import wx
class Ogr2ogr4intoPGUI(ToolCtrlBasePanel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        ToolCtrlBasePanel.__init__(self, *args, **kwds)
        self.itype = "layername"#用路径名字作为输入

        sizer = wx.BoxSizer(wx.VERTICAL)
        #self.chk_ow = wx.CheckBox(self, -1, "-overwrite")

        #sizer.Add( self.chk_ow )
        self.SetSizer(sizer)
        self.Layout()


    def RunTool(self, layers, outSource, outName):
        if len(layers)==1:
            layer = layers[0]
            tool = Ogr2ogr4intoPG(layer, outSource)
            tool.Run()
        else:
            PopMessage(E("layers count must be 1"))
