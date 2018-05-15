# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.6.23; version:1; 创建
"""
该模块定义PostGIS坐标系统的导出
"""

from geosings.ui.commondlg.ToolCtrlBasePanel import *
from geosings.tools.PostGISSrsExp import PostGISSrsExp
import geosings.core.system.UseGetText
from geosings.ui.commondlg.FileSelectCtrl import FileSelectCtrl

import wx,os

class PostGISSrsExpUI(ToolCtrlBasePanel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        ToolCtrlBasePanel.__init__(self, *args, **kwds)
        self.itype = "None"#不需要输入
        #self.otype = "None"#不需要输出
        
        sizer = wx.FlexGridSizer(cols=2,vgap=1,hgap=1)
        txt1 = wx.StaticText(self, -1, _("PostgreSQL bin path")+":")
        self.pgbin = FileSelectCtrl(self, ["psql.exe","psql"], type='dir')
        #self.pgbin = wx.TextCtrl(self, -1)
        txt2 = wx.StaticText(self, -1, _("Host")+":")
        self.host = wx.TextCtrl(self, -1)
        txt3 = wx.StaticText(self, -1, _("Port")+":")
        self.port = wx.TextCtrl(self, -1)
        txt4 = wx.StaticText(self, -1, _("User")+":")
        self.user = wx.TextCtrl(self, -1)
        txt5 = wx.StaticText(self, -1, _("Password")+":")
        self.pwd = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD )
        txt6 = wx.StaticText(self, -1, _("GeoDB")+":")
        self.geodb = wx.TextCtrl(self, -1)
        #txt7 = wx.StaticText(self, -1, _("Output file")+":")
        #self.output = wx.TextCtrl(self, -1)

        sizer.Add( txt1 )
        sizer.Add( self.pgbin )
        sizer.Add( txt2 )
        sizer.Add( self.host )
        sizer.Add( txt3 )
        sizer.Add( self.port )
        sizer.Add( txt4 )
        sizer.Add( self.user )
        sizer.Add( txt5 )
        sizer.Add( self.pwd )
        sizer.Add( txt6 )
        sizer.Add( self.geodb )
        #sizer.Add( txt7 )
        #sizer.Add( self.output )
        self.SetSizer(sizer)
        self.Layout()
        

    def RunTool(self, layers, outSource, outName):
        pgconf = {
            "pgbin":"",
            "user":"postgres",
            "geodb":"geodb",
            }
        if outSource=="":
            PopMessage(E("output file must be set"))
            return
        output = outSource
        if outName is not None and outName != "":
            output = os.path.join(outSource,outName)
        print output
        if self.pgbin.GetValue()!="":
            pgconf['pgbin'] = self.pgbin.GetValue()
        if self.host.GetValue()!="":
            pgconf['host'] = self.host.GetValue()
        if self.port.GetValue()!="":
            pgconf['port'] = self.host.GetValue()
        if self.user.GetValue()!="":
            pgconf['user'] = self.user.GetValue()
        if self.pwd.GetValue()!="":
            pgconf['pwd'] = self.pwd.GetValue()
        if self.geodb.GetValue()!="":
            pgconf['geodb'] = self.geodb.GetValue()
        PostGISSrsExp(pgconf).ExpToTxt(output)
