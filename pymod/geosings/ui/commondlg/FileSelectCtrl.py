# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.6.30; version:1; 创建
"""
该模块定义文件选择控件
"""

import wx
import geosings.core.system.UseGetText

class FileSelectCtrl(wx.Panel):
    def __init__(self, parent, filters, title="Select a File",
            type='file',size=(200,20)):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.filters = filters
        self.title = _(title)
        self.type = type
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "", size=(size[0]-30,size[1]))
        self.button_1 = wx.Button(self, -1, _("..."), size=(30,20))
        #sizer.Add(self.text_ctrl_1,1,wx.EXPAND,0)
        sizer.Add(self.text_ctrl_1)
        sizer.Add(self.button_1)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)

        self.button_1.Bind(wx.EVT_BUTTON, self.__SelectFile)

    def __MakeFilter(self,filters):
        #return "(*.bmp)(*.jpg)|*.bmp;*.jpg|(*.gif)|*.gif"
        name = "".join(["(%s)" % (filter) for filter in filters])
        ext = ";".join(["%s" % (filter) for filter in filters])
        return name+"|"+ext

    def __SelectFile(self,evt):
        dlg = wx.FileDialog(
            None, message=self.title, defaultDir="", 
            defaultFile="", wildcard=self.__MakeFilter(self.filters), style=wx.OPEN
            )
        if dlg.ShowModal()==wx.ID_OK:
            if self.type=="file":
                self.text_ctrl_1.SetValue(dlg.GetPath())
            elif self.type=="dir":
                self.text_ctrl_1.SetValue(dlg.GetDirectory())

    def GetValue(self):
        return self.text_ctrl_1.GetValue()

if __name__=="__main__":
    from TestFrame import RunTest
    RunTest(FileSelectCtrl, ["psql.exe"], type='dir')
    
