import  wx
import  wx.lib.scrolledpanel as scrolled
from geosings.ui.commondlg.OpenDlg import OpenLayerDlg

class TestPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, size, layers, count):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        mainsize = size
        self.layers = layers
        words = []
        for layer in layers:
            words.append( layer.path )
        panel1 = scrolled.ScrolledPanel(self, -1, size=mainsize,
                                 style = wx.TAB_TRAVERSAL|wx.SUNKEN_BORDER, name="panel1" )
        fgs1 = wx.FlexGridSizer(cols=3, vgap=0, hgap=0)
        self.pairs = {}
        words.append(" ")
        if count>len(layers):
            words.extend([" " for i in range(count-len(layers)-1)])

        txtw = len(str(len(words)))*10
        index = 0
        for word in words:
            index+=1
            label = wx.StaticText(panel1, -1, str(index)+":")
            tc = wx.ComboBox(panel1, -1, word, size=(mainsize[0]-40-txtw,20), choices = words)
            but = wx.Button(panel1, -1, "...", size=(20,20))
            but.Bind(wx.EVT_BUTTON, self.EvtBut)
            self.pairs[id(but)] = tc
            fgs1.Add(label, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT)
            fgs1.Add(tc, flag=wx.RIGHT)
            fgs1.Add(but, flag=wx.ALIGN_RIGHT)

        panel1.SetSizer( fgs1 )
        panel1.SetAutoLayout(1)
        panel1.SetupScrolling()

        vbox.Add(panel1, 0, wx.FIXED_MINSIZE)
        self.SetSizer(vbox)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def EvtBut(self, evt):
        dlg = OpenLayerDlg(self)
        dlg.ShowModal()
        but = evt.GetEventObject()
        cb = self.pairs[id(but)]
        cb.SetValue(dlg.GetPath())

    def EvtText(self, evt):
        evt.Skip()

    def GetInputs(self):
        return []

if __name__=="__main__":
    layers = []
    from geosings.core.Layer import Layer
    layers.append(Layer.Open("e:/gisdata/data/part.shp"))
    layers.append(Layer.Open("e:/gisdata/data/lines.shp"))

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = wx.Frame(None)
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(TestPanel(frame_1,(300,100),layers,50),1,wx.EXPAND,0)
    frame_1.SetSizer(sizer)
    frame_1.SetAutoLayout(True)
    frame_1.Layout()
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
