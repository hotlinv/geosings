#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该模块定义链接表的Panel

 - writer:linux_23; create: Fri Sep 14 15:58:55 2007 ; version:1; 创建
"""
import wx
import wx.lib.hyperlink as hl

class CondBar(wx.Panel):
    def __init__(self, parent, rs):
        wx.Panel.__init__(self, parent, -1)
        pass
        self.SetBackgroundColour(wx.WHITE)

class HListPanel(wx.Panel):
    def __init__(self, parent, rs=None):
        wx.Panel.__init__(self, parent, -1)
        #wx.ScrolledWindow.__init__(self, parent, -1)
        self.rs = rs
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.condBar = CondBar(self,rs)
        #self.sizer.Add((2,5))
        self.SetRecordset(rs)
        self.sizer.Add(self.condBar)
        self.SetBackgroundColour(wx.WHITE)

        #设置滚动条
        #self.EnableScrolling(True,True)
        #self.SetVirtualSize((100, 100))
        #self.SetScrollRate(20,20)
        
        self.SetSizer(self.sizer)  
        self.SetAutoLayout(True)
        self.Layout()
        self.sizer.Fit(parent)
        

    def SetRecordset(self,rs):
        if rs is None:
            return
        for r in rs:
            hyper = hl.HyperLinkCtrl(self, wx.ID_ANY,
                                            r[0],
                                            URL=r[2])
            hyper.SetBackgroundColour(wx.WHITE)
            hyper.Bind(hl.EVT_HYPERLINK_LEFT, r[3])
            hyper.AutoBrowse(False)
            self.sizer.Add(hyper, 0, \
                    wx.LEFT|wx.RIGHT|wx.TOP, 14)

            _context = wx.StaticText(self, -1, r[1])
            self.sizer.Add(_context, 0, wx.LEFT|wx.RIGHT, 30)
            self.sizer.Add((10,5))

        self.Layout()
        self.sizer.FitInside(self.GetParent())

    def OnLink(self,evt):
        opid = id(evt.GetEventObject())
        #print opid
        if opid in self.foos:
            self.foos[opid]()

if __name__=="__main__":
    from TestFrame import RunTest
    RunTest(HListPanel,[["aaa","context1\nsadf\nhahaha",""],
                    ["bbb","conte\nxt2",""],
                    ["ccc","a,b\nafsad\n\nsdftt\n",""],
                    ["ddd","a\nb\nc\nd",""]
                    ])
