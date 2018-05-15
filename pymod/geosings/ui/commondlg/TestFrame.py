# -*- coding: utf-8 -*-

import wx
def RunTest(PanelClass, *args, **kwds):
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = wx.Frame(None)
    sizer = wx.BoxSizer(wx.VERTICAL)
    panel = PanelClass(frame_1, *args, **kwds)
    sizer.Add(panel,1,wx.EXPAND,0)
    frame_1.SetSizer(sizer)
    frame_1.SetAutoLayout(True)
    frame_1.Layout()
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
    print "test end"

def RunDlgTest(DlgClass, *args, **kwds):
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = DlgClass(None, *args, **kwds)
    app.SetTopWindow(frame_1)
    frame_1.ShowModal()
    print "test end"
