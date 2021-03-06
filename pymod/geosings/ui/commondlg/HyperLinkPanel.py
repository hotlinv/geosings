# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.6.25; version:1; 创建
"""动态链接Panel
"""

import wx
import wx.lib.hyperlink as hl
from geosings.ui.core.UIConst import ActionResult

def testfoo(evt):
    print dir(evt)
    print evt.GetClientData()

class HyperLinkDlg(wx.Dialog):
    def __init__(self, parent, name, links):
        wx.Dialog.__init__(self, parent, -1,
                style=wx.NO_3D)
        sizer = wx.BoxSizer(wx.VERTICAL)
        hl = HyperLinkPanel(self, name, links)
        self.panel = hl
        sizer.Add(hl,1,wx.EXPAND,0)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.SetSizeHints(self)
        self.Layout()
        hl.Bind(wx.EVT_LEAVE_WINDOW,self.OnHLLeave)

    def OnHLLeave(self, evt):
        rect = self.GetClientRect()
        x,y = self.ClientToScreenXY(rect.GetLeft(),rect.GetTop())
        pos = wx.GetMousePosition()
        newrect = wx.Rect(x,y,rect.GetWidth(),rect.GetHeight())
        if not newrect.Inside(pos):
            self.Show(False)

class HyperLinkPanel(wx.Panel):
    def __init__(self, parent, name, hllist):
        wx.Panel.__init__(self, parent, -1)

        self.name = name
        self.hllist = hllist
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)  
        sizer.Add((2,5))
        sizer.Add(wx.StaticText(self,-1,name), 1,
                wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 20)
        sizer.Add((2,5))

        for hlconf in self.hllist:
            self._hyper = hl.HyperLinkCtrl(self, wx.ID_ANY,
                                            hlconf['name'],
                                            URL="")
            sizer.Add(self._hyper, 0, wx.ALIGN_CENTER_HORIZONTAL| \
                    wx.LEFT|wx.RIGHT, 20)
            self._hyper.Bind(hl.EVT_HYPERLINK_LEFT, self.OnLink)
            self._hyper.SetToolTip(wx.ToolTip(hlconf["tooltip"]))
            self._hyper.AutoBrowse(False)
            sizer.Add((10,5))

    def OnLink(self, evt):
        #print 'link'
        from geosings.ui.core.Brain import msgParser
        opname = evt.GetEventObject().GetLabel()
        for hlconf in self.hllist:
            #print hlconf['name'], opname
            if opname == hlconf['name']:
                msgParser.SendMsg(hlconf['foo']+" "+self.name)
                result = msgParser.result
                if result==ActionResult.UpdateAll:
                    from geosings.ui.PyMainPanel import GetMainPanel
                    GetMainPanel().canvas.ReDraw()
                endfoo,endfooargs = None,None
                if 'end' in hlconf:
                    endfoo = hlconf['end']
                if 'endargs' in hlconf:
                    endfooargs = hlconf['endargs']
                if endfoo:
                    if endfooargs:
                        endfoo(endfooargs)
                    else:
                        endfoo()
                break

if __name__== "__main__":
    from TestFrame import RunTest
    links = [
            {'name':u"移除",'foo':testfoo,'tooltip':u"移除这个图层"},
            {'name':u"统计",'foo':testfoo,'tooltip':u"统计这个图层"},
            ]
    RunTest(HyperLinkPanel,u"haha",links)
