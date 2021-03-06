#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该模块定义叠加操作工具操作界面

 - writer:linux_23; create: Wed Nov 14 21:11:55 2007 ; version:1; 创建
"""
from geosings.ui.commondlg.ToolCtrlBasePanel import *
import geosings.core.system.UseGetText
from geosings.core.Layer import Layer
from geosings.ui.commondlg.LayersPanel import LayersPanel
from geosings.ui.commondlg.FileSelectCtrl import FileSelectCtrl
from geosings.tools.Overlay import *

import wx,os

class IntersectionUI(ToolCtrlBasePanel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        ToolCtrlBasePanel.__init__(self, *args, **kwds)
        
        sizer = wx.FlexGridSizer(cols=2,vgap=1,hgap=1)
        self.SetSizer(sizer)
        self.Layout()

    def RunTool(self, layers, outSource, outName):
        if len(layers)!=2:
            PopMessage(E("please select 2 layers"))
            return
        l1,l2 = layers[0],layers[1]
        if type(l1)=='str' or type(l1)=='unicode':
            l1 = Layer.Open(l1)
        if type(l2)=='str' or type(l2)=='unicode':
            l2 = Layer.Open(l2)
        Intersection(l1,l2,outSource,outName)


