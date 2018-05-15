# -*- coding: utf-8 -*-
"""该模块定义选择路径对话框
"""

import wx

class SelPathDlg(wx.Dialog):
    """路径选择对话框
    """
    def __init__(self,parent):
        """初始化对话框
        @type parent: wxCtrl
        @param parent: 父框架
        """
        wx.Dialog.__init__(self,parent,-1)
        self.path = ""
        self.dir1 = wx.GenericDirCtrl(self, -1, size = (200,300),style=0)
        self.but = wx.Button(self,wx.ID_OK,"&OK")

        sz = wx.BoxSizer(wx.VERTICAL)
        sz.Add((35, 35))  # some space above

        sz.Add(self.dir1, 0, wx.EXPAND,wx.ALL,10)

        sz.Add((35,35))

        sz.Add(self.but, 0, wx.ALIGN_CENTER)

        self.SetSizer(sz)
        self.SetAutoLayout(True)
        self.Layout()

        #self.but.Bind(wx.EVT_BUTTON, self.OnSel)
        wx.EVT_BUTTON( self, wx.ID_OK, self.OnSel)

    def OnSel(self,evt):
        """选择路径的按钮响应
        @type evt: wxEvent
        @param evt: EVT_BUTTON事件
        """
        #if self.path is not None:
        self.path = self.dir1.GetPath()
        print self.path
        if self.Validate():
            self.EndModal(wx.ID_OK)
            self.Destroy()

    def GetPath(self):
        """获取选择的路径
        @rtype: str
        @return: 路径
        """
        return self.path
        
def testApp():
    """测试
    """
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = SelPathDlg(None)
    app.SetTopWindow(frame_1)
    frame_1.ShowModal()
    print frame_1.GetPath()

if __name__ == "__main__":
    testApp()
