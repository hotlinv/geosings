# -*- encoding: utf-8 -*-
"""定义数据打开对话框

2008.9.3 linux_23
"""

import wx
import os,sys
from geosings.ui.core.MainImage import GetFormatImageList
import geosings.core.system.UseGetText

class DataValidater:
    def is_dataset(self, path):
        return False
    def is_layer(self, path):
        return False
class ShapefileValidater(DataValidater):
    def is_dataset(self,path):
        if os.path.isdir(path):
            return True
        return False
    def is_layer(self, path):
        if path.endswith('shp'):
            return True
        return False
class MapInfoValidater(DataValidater):
    def is_dataset(self, path):
        if os.path.isdir(path):
            return True
        return False
    def is_layer(self, path):
        if path.endswith('tab'):
            return True
        return False
class GeoTiffValidater(DataValidater):
    def is_dataset(self, path):
        if os.path.isdir(path):
            return True
        return False
    def is_layer(self, path):
        if path.endswith('tif'):
            return True
        return False
def get_validter(name):
    if name=='shp':
        return ShapefileValidater()
    elif name=='tab':
        return MapInfoValidater()
    elif name=='tif':
        return GeoTiffValidater()
    else:
        return DataValidater()

class DataListCtrl(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.il,self.imghs = GetFormatImageList()
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, _("Data list"))
        self.SetColumnWidth(0, 500)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.LeftClick)
        self.value = ""
    def LeftClick(self, evt):
        item = evt.GetItem()
        sel = item.GetText()
        self.value = sel
    def GetValue(self):
        return self.value

class DSListCtrl(wx.ListCtrl):
    def __init__(self, parent, child):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.child = child
        self.il,self.imghs = GetFormatImageList()
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, _("Data Source list"))
        self.SetColumnWidth(0, 300)
        self.thisds = ""
        self.__InitList()
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.LeftDClick)
    def GetValue(self):
        return self.thisds[1:]
    def __InitList(self):
        from geosings.core.system import GetLogicalDriveStrings
        drilist = GetLogicalDriveStrings()
        for dri in drilist:
            index = self.InsertImageStringItem(sys.maxint, dri,
                    self.imghs["source"])
    def LeftDClick(self,event):
        item = event.GetItem()
        sel = item.GetText()
        self.__ListFileSystem(sel)
    def __ListFileSystem(self, sel=""):
        self.DeleteAllItems()
        if self.child:
            self.child.DeleteAllItems()
        index = self.InsertImageStringItem(sys.maxint, '..',
                self.imghs["dir"])
        if sel == "":
            self.thisds = "/"
            self.__InitList()
        elif sel == ".." and self.thisds == '/':
            self.DeleteAllItems()# delete ..
            self.mode = ""
            self.thisds = ""
            self.__InitList()
        elif sel == "..":
            path,d  = os.path.split(self.thisds[1:])
            if d == '':
                self.__ListFileSystem("")
                return
            self.__ListSomeDir(path)
        else:
            path = os.path.join(self.thisds[1:],sel)
            self.__ListSomeDir(path)
    def __ListSomeDir(self,path):
        """列出某个目录下的数据列表
        """
        if not os.path.isdir(path):
            self.InsertStringItem(sys.maxint, path)
            return 
        dirpath = os.listdir(path)
        self.thisds = '/'+path
        for tmpf in dirpath:
            path = os.path.join(self.thisds, tmpf)[1:]
            if self.GetParent().v.is_dataset(path):
                index = self.InsertImageStringItem(sys.maxint, tmpf,
                        self.imghs["dir"])
            elif self.GetParent().v.is_layer(path) and self.child:
                index = self.child.InsertImageStringItem(sys.maxint, tmpf,
                        self.imghs["feature"])

class DataSelPanel(wx.Panel):
    def __init__(self, parent, dtype="", sl=True):
        """dtype是数据类型
        sl是要不要选择图层
        """
        wx.Panel.__init__(self,parent, -1)
        types = ['shp','tab','tif']
        vsizer = wx.BoxSizer(wx.VERTICAL)
        self.v = get_validter(dtype)
        if dtype not in types:
            self.typesel = wx.ComboBox(
                self, 500, types[0], (90, 50), 
                (95, -1), types, wx.CB_DROPDOWN #|wxTE_PROCESS_ENTER
                )
            vsizer.Add(self.typesel, 0, wx.EXPAND|wx.ALL, 20)
            self.v = get_validter(types[0])
            self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.typesel)
            
        sizermain = wx.BoxSizer(wx.HORIZONTAL)
        if sl:
            self.dl = DataListCtrl(self)
        else:
            self.dl = None

        self.dsl = DSListCtrl(self, self.dl)
        sizermain.Add(self.dsl, 1, wx.EXPAND|wx.ALL, 10)
        if sl:
            sizermain.Add(self.dl, 1, wx.EXPAND|wx.ALL, 10)
            self.dl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.SelectLayer)
        vsizer.Add(sizermain, 1, wx.EXPAND|wx.ALL, 10)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.butd = wx.Button(self,-1, _("Open dataset"))
        self.butl = wx.Button(self,-1, _("Open layout"))
        self.SelectDatasetFoo = None
        self.SelectLayerFoo = None
        self.Bind(wx.EVT_BUTTON, self.SelectDataset, self.butd)
        self.Bind(wx.EVT_BUTTON, self.SelectLayer, self.butl)
        hsizer.Add(self.butd, 1, wx.EXPAND|wx.ALL, 10)
        hsizer.Add(self.butl, 1, wx.EXPAND|wx.ALL, 10)
        vsizer.Add(hsizer, 0, wx.EXPAND|wx.ALL, 10)

        self.SetAutoLayout(True)
        self.SetSizer(vsizer)
        self.Layout()
    def EvtComboBox(self, evt):
        #cb = evt.GetEventObject()
        #data = cb.GetClientData(evt.GetSelection())
        #self.log.WriteText('EvtComboBox: %s\nClientData: %s\n' % (evt.GetString(), data))

        #if evt.GetString() == 'one':
        #    self.log.WriteText("You follow directions well!\n\n")
        self.v = get_validter(evt.GetString())

    def SelectDataset(self, evt):
        if self.SelectDatasetFoo:
            self.SelectDatasetFoo(self.dsl.GetValue())
    def SelectLayer(self, evt):
        if self.SelectLayerFoo:
            if self.dl:
                self.SelectLayerFoo(self.dsl.GetValue(),self.dl.GetValue())

class DataFrame(wx.Frame):
    def __init__(self, parent, name, dtype="", dl=True):
        wx.Frame.__init__(self, parent, -1, name)
        self.mainp = DataSelPanel(self, dtype, dl)
        sizermain = wx.BoxSizer(wx.VERTICAL)
        sizermain.Add(self.mainp, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizermain)
        self.Layout()
        self.SetSize((600,400))
    def RegSelectDatasetFoo(self, foo):
        self.mainp.SelectDatasetFoo = foo
    def RegSelectLayerFoo(self, foo):
        self.mainp.SelectLayerFoo = foo


if __name__=="__main__":
    def printds(val):
        print val
    def printly(ds, ly):
        print ds, ly
    app = wx.PySimpleApp(0)
    mainframe = DataFrame(None, _("Open some data"))
    mainframe.RegSelectDatasetFoo( printds )
    mainframe.RegSelectLayerFoo( printly )
    app.SetTopWindow(mainframe)
    mainframe.Show()
    app.MainLoop()

