import wx
from geosings.ui.commondlg.DSListCtrl import DSListDialog
from geosings.core.system.EncodeTran import utf82locale

class OutputPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "")
        self.button_1 = wx.Button(self, -1, "...", size=(30,20))
        self.text_ctrl_2 = wx.TextCtrl(self, -1, "")

        self.button_1.Bind(wx.EVT_BUTTON, self.SelectSource)

        self.__do_layout()
        # end wxGlade

    def SelectSource(self, evt):
        dlg = DSListDialog(self, -1, _("Select a DataSource"))
        dlg.ShowModal()
        self.text_ctrl_1.SetValue(dlg.GetSelected())

    def __do_layout(self):
        # begin wxGlade: MyPanel.__do_layout
        #sizer_1 = wx.FlexGridSizer(cols=3, vgap=4, hgap=4)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.text_ctrl_1, 1, wx.EXPAND,2)
        sizer_1.Add(self.button_1, 0, wx.ADJUST_MINSIZE, 2)
        sizer_1.Add(self.text_ctrl_2, 0, wx.ADJUST_MINSIZE, 2)
        self.SetAutoLayout(True)
        sizer_2.Add(sizer_1, 0, wx.EXPAND, 2)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        sizer_2.SetSizeHints(self)
        # end wxGlade
    def GetOutputSource(self):
        return utf82locale(self.text_ctrl_1.GetValue())
    def GetOutputName(self):
        return utf82locale(self.text_ctrl_2.GetValue())

# end of class MyPanel

if __name__=="__main__":
    from TestFrame import RunTest
    RunTest(OutputPanel, -1)
