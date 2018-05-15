import wx,sys
import  wx.lib.popupctl as  pop
from geosings.ui.commondlg.OpenDlg import OpenLayerDlg
from geosings.core.Layer import Layer
from geosings.core.system.EncodeTran import utf82locale

class PopupWin(wx.Dialog):
    def __init__(self, laynamelist, parent):
        wx.Dialog.__init__(self,parent,-1,style=wx.NO_3D)

        self.win = wx.Window(self,-1,pos = (0,0),style = 0)

        self.laylist = laynamelist
        self.st = wx.ListBox(self.win, -1, style=wx.LB_HSCROLL,
                          choices=laynamelist,
                          pos=(0,0))

        sz = self.st.GetBestSize()
        #sz = (200,100)
        self.win.SetSize( sz )
        self.st.SetSize( sz )
        self.SetSize( sz )
        #self.SetSize((100,100))

        #self.SetContent(self.win)

        self.st.Bind(wx.EVT_LISTBOX, self.OnSelected)

        #wx.CallAfter(self.Refresh)


    def OnSelected(self, evt):
        path = evt.GetString()
        print path
        self.GetParent().SetLayerPath(path)
        self.Show(False)
        self.Destroy()
        self.GetParent().popwin = None
        evt.Skip()
    
class LayersPanel(wx.Panel):
    def __init__(self, parent, size, layers):
        # begin wxGlade: MyPanel.__init__
        #kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, parent, -1, size=size)

        mainsize = size
        self.layers = layers
        self.words = []
        for layer in layers:
            self.words.append( layer.path )
        #fgs1 = wx.FlexGridSizer(cols=3, vgap=0, hgap=0)
        txtw = len(str(len(self.words)))*10
        self.layersid = []
        self.namesid = []
        self.popwin = None

        self.layer_list = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_HRULES)
        self.layer_list.InsertColumn(0, "", wx.LIST_FORMAT_RIGHT);
        self.layer_list.InsertColumn(1, _("ID"), wx.LIST_FORMAT_RIGHT);
        self.layer_list.InsertColumn(2, _("Layer"));
        self.layer_list.SetColumnWidth(0, 0);
        self.layer_list.SetColumnWidth(1, 30);
        self.layer_list.SetColumnWidth(2, self.GetSize()[0]-40);
        self.index = 0
        for word in self.words:
            self.index+=1
            item = self.layer_list.InsertStringItem(sys.maxint, "")
            self.layer_list.SetStringItem(item, 1, str(self.index))
            self.layer_list.SetStringItem(item, 2, word)
            self.layersid.append(item)

        self.but_add = wx.Button(self, -1, _("+"), size=(20,20))
        self.but_set = wx.Button(self, -1, _("..."), size=(20,20))
        self.but_sub = wx.Button(self, -1, _("X"), size=(20,20))
        self.but_down = wx.Button(self, -1, _("v"), size=(20,20))
        self.but_up = wx.Button(self, -1, _("^"), size=(20,20))
        self.but_sel = wx.Button(self, -1, _("?"), size=(20,20))
        #self.but_sel = wx.TextCtrl(self, -1, "asdf", size=(20,20))
        #self.but_sel = PopupWin(self.words,self,-1)

        self.but_add.Bind(wx.EVT_BUTTON, self.Add)
        self.but_set.Bind(wx.EVT_BUTTON, self.Set)
        self.but_sub.Bind(wx.EVT_BUTTON, self.Sub)
        self.but_up.Bind(wx.EVT_BUTTON, self.Up)
        self.but_down.Bind(wx.EVT_BUTTON, self.Down)
        self.but_sel.Bind(wx.EVT_BUTTON, self.Select)

        self.__do_layout()

        # end wxGlade
    def __do_layout(self):
        # begin wxGlade: MyPanel.__do_layout
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.layer_list, 1, wx.EXPAND, 0)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.but_add, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.but_set, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.but_sel, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.but_sub, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.but_down, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(self.but_up, 0, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(sizer_2, 0, wx.ADJUST_MINSIZE, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        # end wxGlade

    def Add(self, evt):
        dlg = OpenLayerDlg(self)
        dlg.ShowModal()
        path = dlg.GetPath()
        if path!="":
            item = self.layer_list.InsertStringItem(sys.maxint, "")
            self.layer_list.SetStringItem(item, 1, str(self.index+1))
            self.layer_list.SetStringItem(item, 2, path)
            self.index+=1

    def __GetSelectedItem(self):
        return self.layer_list.GetNextItem(-1, wx.LIST_NEXT_ALL,
                wx.LIST_STATE_SELECTED)

    def Sub(self, evt):
        item = self.__GetSelectedItem()
        if item != -1:
            self.layer_list.SetStringItem(item, 2, "")
    def Set(self, evt):
        item = self.__GetSelectedItem()
        if item != -1:
            dlg = OpenLayerDlg(self)
            dlg.ShowModal()
            path = dlg.GetPath()
            if path !="":
                self.layer_list.SetStringItem(item, 2, path)
    def Up(self, evt):
        item = self.__GetSelectedItem()
        if item != -1:
            pass
    def Down(self, evt):
        item = self.__GetSelectedItem()
        if item != -1:
            pass

    def SetLayerPath(self, path):
        item = self.__GetSelectedItem()
        if item != -1 :
            if path !="":
                self.layer_list.SetStringItem(item, 2, path)
    def Select(self, evt):
        item = self.__GetSelectedItem()
        if item != -1 and self.popwin is None:
            self.popwin = PopupWin(self.words,self)

            btn = evt.GetEventObject()
            pos = btn.ClientToScreen( (0,0) )
            sz =  btn.GetSize()
            self.popwin.Move((pos.x,pos.y+sz[1]))

            self.popwin.Show(True)
        elif self.popwin is not None:
            self.popwin.Show(False)
            self.popwin.Destroy()
            self.popwin = None
            pass

    def GetOpenedLayers(self):
        olayers = []
        item = self.layer_list.GetNextItem(-1, wx.LIST_NEXT_ALL,
                wx.LIST_STATE_DONTCARE)
        while item!=-1:
            layerpath = utf82locale(self.layer_list.GetItem(item,2).GetText())
            if layerpath!="" and layerpath!=u"":
                layer = Layer.Open(layerpath)
                olayers.append(layer)
            item = self.layer_list.GetNextItem(item, wx.LIST_NEXT_ALL,
                    wx.LIST_STATE_DONTCARE)
        return olayers

    def GetOpenedLayersName(self):
        olayers = []
        item = self.layer_list.GetNextItem(-1, wx.LIST_NEXT_ALL,
                wx.LIST_STATE_DONTCARE)
        while item!=-1:
            layerpath = utf82locale(self.layer_list.GetItem(item,2).GetText())
            if layerpath!="" and layerpath!=u"":
                olayers.append(layerpath)
            item = self.layer_list.GetNextItem(item, wx.LIST_NEXT_ALL,
                    wx.LIST_STATE_DONTCARE)
        return olayers


# end of class MyPanel

if __name__=="__main__":
    layers = []
    from geosings.core.Layer import Layer
    layers.append(Layer.Open("e:/gisdata/data/part.shp"))
    layers.append(Layer.Open("e:/gisdata/data/lines.shp"))
    from TestFrame import RunTest
    RunTest(LayersPanel,(300,100),layers)

