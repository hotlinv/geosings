# -*- encoding: utf-8 -*-
"""定义实用工具对话框模板。
"""
import wx
from OutputPanel import OutputPanel
from LayersPanel import LayersPanel
from geosings.core.system import MyOutForUIText
from geosings.core.Exception import *

class ToolTemplatePanel(wx.Panel):
    def __init__(self, layers, toolPaneClassName, tool_init_args, *args, **kwds):
        # begin wxGlade: MyPanel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.ctrlpane = apply(toolPaneClassName, [self,]+tool_init_args)
        if self.ctrlpane.itype==None or self.ctrlpane.itype=="None":
            self.input = None
        else:
            self.input = LayersPanel(self, (300, 125), layers)
        if hasattr(self.ctrlpane,'otype'):
            if self.ctrlpane.otype==None or \
                self.ctrlpane.otype=="None":
                self.output = None
            else:
                self.output = OutputPanel(self, -1)
        else:
            self.output = OutputPanel(self, -1)
        self.infoctrl = wx.TextCtrl(self, -1, "", size=(125, 130),style=wx.TE_MULTILINE)
        self.__do_layout()
        # end wxGlade
    def __do_layout(self):
        # begin wxGlade: MyPanel.__do_layout
        #sizer_1 = wx.FlexGridSizer(cols=3, vgap=4, hgap=4)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        if self.input is not None:
            boxinput = wx.StaticBox(self, -1, _("Input"))
            bisizer = wx.StaticBoxSizer(boxinput, wx.VERTICAL)
            bisizer.Add(self.input, 1, wx.EXPAND|wx.ALL, 3)
            sizer_1.Add(bisizer, 0, wx.EXPAND|wx.ALL,5)
        boxctrl = wx.StaticBox(self, -1, _("Control"))
        bcsizer = wx.StaticBoxSizer(boxctrl, wx.VERTICAL)
        bcsizer.Add(self.ctrlpane, 1, wx.EXPAND|wx.ALL, 3)
        sizer_1.Add(bcsizer, 0, wx.EXPAND|wx.ALL,5)
        if self.output is not None:
            boxoutput = wx.StaticBox(self, -1, _("Output"))
            bosizer = wx.StaticBoxSizer(boxoutput, wx.VERTICAL)
            bosizer.Add(self.output, 1, wx.EXPAND|wx.ALL, 3)
            sizer_1.Add(bosizer, 0, wx.EXPAND|wx.ALL, 5)
        static_line_3 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        sizer_1.Add(static_line_3, 0, wx.EXPAND|wx.ALL, 5)
        sizer_1.Add(self.infoctrl, 0, wx.EXPAND|wx.ALL, 5)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        # end wxGlade

    def RunTool(self):
        if self.ctrlpane.itype=="layer":
            inputs = self.input.GetOpenedLayers()
        elif self.ctrlpane.itype==None or \
                self.ctrlpane.itype=='None':
            inputs = None
        else:
            inputs = self.input.GetOpenedLayersName()
            #这边已经经过LayersPanel的编码转换，不需要再转
        #下面需要再转换
        if self.output is not None:
            osource = self.output.GetOutputSource()
            oname = self.output.GetOutputName()
        else:
            osource = None
            oname = None
        #把打印位置定位到TextCtrl
        printctrl = MyOutForUIText(self.infoctrl)
        try:
            self.ctrlpane.RunTool(inputs, osource, oname)
        except ToolRunFailErr,e: 
            print _("Failure"), e.GetMessage()
            printctrl.ResetStd()
        else:
            print _("Success")
            printctrl.ResetStd()

# end of class MyPanel
class ToolDialog(wx.Dialog):
    """工具对话框的主对话框
    """
    def __init__(self, layers, toolPaneClassName, tool_init_args, *args, **kwds):
        """初始化对话框
        """
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER|wx.MINIMIZE_BOX| \
                wx.MAXIMIZE_BOX|wx.SYSTEM_MENU|wx.RESIZE_BORDER#|wx.FRAME_TOOL_WINDOW
        wx.Dialog.__init__(self, *args, **kwds)
        self.mainpanel = ToolTemplatePanel(layers,
                toolPaneClassName, tool_init_args, self, -1)
        self.static_line_3 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        self.butOK = wx.Button(self, wx.ID_OK, _("Go"))
        self.butCANCEL = wx.Button(self, wx.ID_CANCEL, _("Close"))
        
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        #sizer_11 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add((20,20))
        sizer_1.Add(self.mainpanel, 1, wx.EXPAND, 0)
        sizer_1.Add(self.static_line_3, 0, wx.ALL|wx.EXPAND, 4)
        sizer_2.Add(wx.Panel(self,-1), 1, wx.EXPAND, 0)
        sizer_2.Add(self.butOK, 0, wx.FIXED_MINSIZE|wx.ALL, 5)
        sizer_2.Add(self.butCANCEL, 0, wx.FIXED_MINSIZE|wx.ALL, 5)
        sizer_1.Add(sizer_2, 0, wx.EXPAND|wx.ALL,5)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        self.Layout()
        
        wx.EVT_BUTTON( self, wx.ID_OK, self.OnOK )
        wx.EVT_BUTTON( self, wx.ID_CANCEL, self.OnCancel )

    def OnOK(self,evt):
        """ok按钮的响应
        @type evt: wxEvent
        @param evt: OK按钮事件
        """
        self.mainpanel.RunTool()
        #self.EndModal(wx.ID_OK)
        #self.Destroy()

    def OnCancel(self,evt):
        """Cancel按钮的响应
        @type evt: wxEvent
        @param evt: Cancel按钮事件
        """
        self.EndModal(wx.ID_CANCEL)
        self.Destroy()

if __name__=="__main__":
    from TestFrame import RunTest
    from geosings.core.Layer import Layer
    layers = []
    layers.append(Layer.Open("e:/gisdata/data/part.shp"))
    #RunTest(ToolTemplatePanel, -1)
    
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dlg = ToolDialog(layers, wx.Panel, [-1], None, -1, "")
    app.SetTopWindow(dlg)
    ret = dlg.ShowModal()
    app.MainLoop()
    print "end"

