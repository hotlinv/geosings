# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.6.29; version:1; 创建
"""
该模块定义投影设置功能操作界面
"""
from geosings.ui.commondlg.ToolCtrlBasePanel import *
from geosings.tools.SetCoorSys import *
import geosings.core.system.UseGetText
from geosings.core.Layer import Layer
from geosings.ui.commondlg.FileSelectCtrl import FileSelectCtrl

import wx,os

class SetCoorSysUI(ToolCtrlBasePanel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        ToolCtrlBasePanel.__init__(self, *args, **kwds)
        #self.itype = "None"#不需要输入
        #self.otype = "None"#不需要输出
        
        sizer = wx.FlexGridSizer(cols=2,vgap=1,hgap=1)
        txt1 = wx.StaticText(self, -1, _("Coordinate system file")+":")
        self.crfile = FileSelectCtrl(self, ["*.prj"])

        sizer.Add( txt1 )
        sizer.Add( self.crfile )
        self.SetSizer(sizer)
        self.Layout()

    def RunTool(self, layers, outSource, outName):
        if self.crfile.GetValue()=="":
            PopMessage(E("please select a prj file"))
            return
        if outSource=="" or outSource is None:
            PopMessage(E("please select a path for output"))
            return
        file = open(self.crfile.GetValue())
        wkt = file.read()
        file.close()
        for layer in layers:
            l = layer
            if type(layer)=='str' or type(layer)=='unicode':
                l = Layer.Open(layer)
            SetCoorSysByWkt(l,wkt,outSource)
