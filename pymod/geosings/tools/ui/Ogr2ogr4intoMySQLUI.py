# -*- coding: utf-8 -*-

"""
该模块定义Ogr2ogr4intoMySQL工具的UI定义
"""
from geosings.ui.commondlg.ToolCtrlBasePanel import *
from geosings.tools.Ogr2ogr import Ogr2ogr4intoMySQL
from geosings.core.system.EncodeTran import utf82locale

import wx
class Ogr2ogr4intoMySQLUI(ToolCtrlBasePanel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        ToolCtrlBasePanel.__init__(self, *args, **kwds)
        self.itype = "layername"#用路径名字作为输入
        self.def_engine_txt = _("default engine")

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.chk_update = wx.CheckBox(self, -1, "-update")
        self.chk_ow = wx.CheckBox(self, -1, "-overwrite")
        self.cb_engine = wx.ComboBox(
            self, 500, self.def_engine_txt, (190, 50), 
            (195, -1), ["MyISAM"], wx.CB_DROPDOWN #|wxTE_PROCESS_ENTER
            )
        self.chk_spatialindex = wx.CheckBox(self, -1, _("build spatial index"))
        self.chk_spatialindex.SetValue(True)
        

        sizer.Add( self.chk_update )
        sizer.Add( self.chk_ow )
        sizer.Add( self.cb_engine )
        sizer.Add( self.chk_spatialindex )
        self.SetSizer(sizer)
        self.Layout()


    def RunTool(self, layers, outSource, outName):
        if len(layers)==1:
            layer = layers[0]
            tool = Ogr2ogr4intoMySQL(layer, outSource)
            if outName != "":
                tool.SetNewName(outName)
            #print self.chk_update.GetValue()
            if self.chk_update.GetValue():
                tool.SetUpdate()
            if self.chk_ow.GetValue():
                tool.SetOverWrite()
            if not self.chk_ow.GetValue():
                tool.SetBuildSpatialIndex(False)
            engine_txt = self.cb_engine.GetValue()
            if engine_txt!=self.def_engine_txt and engine_txt!="":
                tool.SetEngine( utf82locale(engine_txt))
            tool.Run()
        else:
            PopMessage(E("layers count must be 1"))
