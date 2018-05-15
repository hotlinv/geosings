#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.4.1 on Sat Mar 10 13:21:10 2007

import wx,sys,os
import ogr,gdal
from geosings.core.system.RunSysConf import RunSysConf
from geosings.core.DataSet import *
from geosings.ui.core.MainImage import GetFormatImageList
from geosings.core.system.EncodeTran import utf82locale

FILE_SYS = _("local file system")
DB_SYS = _("database")
WEB_SYS = _("web datasource")


class DSListCtrl(wx.ListCtrl):
    def __init__(self, *args, **kwds):
        wx.ListCtrl.__init__(self, *args, **kwds )
        self.dsconf = [FILE_SYS, DB_SYS, WEB_SYS]
        self.il,self.imghs = GetFormatImageList()
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, _("Datalist"))
        self.InsertColumn(1, _("DataType"))
        self.__InitList()

        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)

        self.thisds = ""

        self.mode = None

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.LeftDClick)

    def __InitList(self):
        for dstype in self.dsconf:
            index = self.InsertImageStringItem(sys.maxint, dstype,
                    self.imghs["source"])

    def LeftDClick(self,event):
        item = event.GetItem()
        sel = item.GetText()
        if sel == FILE_SYS and self.thisds=="":
            self.__ListFileSystem()
        elif sel == DB_SYS and self.thisds=="":
            self.__ListDBSystem()
        elif sel == WEB_SYS and self.thisds=="":
            self.__ListWebSystem()
        elif self.mode == FILE_SYS:
            self.__ListFileSystem(sel)
        elif self.mode == DB_SYS:
            self.__ListDBSystem(sel)
        elif self.mode == WEB_SYS:
            self.__ListWebSystem(sel)

    def __ReadLocalDriver(self):
        from geosings.core.system import GetLogicalDriveStrings
        return GetLogicalDriveStrings()

    def __ListFileSystem(self, sel=""):
        self.DeleteAllItems()
        index = self.InsertImageStringItem(sys.maxint, '..',
                self.imghs["dir"])
        if sel == "":
            self.mode = FILE_SYS
            self.thisds = "/"
            dirpath = self.__ReadLocalDriver()
            for files in dirpath:
                index = self.InsertImageStringItem(sys.maxint, files,
                        self.imghs["dir"])
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
        fds,rds,dirs = ListFileSysData(path)
        self.__ListDatas(fds,rds,dirs)
        self.thisds = '/'+path

    def __ListDBType(self):
        dbtypes = DBConfManager.GetDBTypes()
        for type in dbtypes:
            index = self.InsertImageStringItem(sys.maxint, type,
                    self.imghs["database"])
            self.SetStringItem(index,1,_('database'))
    def __ListDB(self, type):
        dbconf = DBConfManager(type)
        for db in dbconf.GetDBList():
            index = self.InsertImageStringItem(sys.maxint, db,
                    self.imghs["database"])
            self.SetStringItem(index, 1,_("database"))
        
    def __ListDBSystem(self, sel=""):
        self.DeleteAllItems()
        index = self.InsertImageStringItem(sys.maxint, '..',
                self.imghs["database"])
        #print self.mode
        if sel == "":
            self.mode = DB_SYS
            self.thisds = "/"
            self.__ListDBType()
        elif sel==".." and self.thisds == "/":
            self.DeleteAllItems()# delete ..
            self.mode = ""
            self.thisds = ""
            self.__InitList()
        elif sel == "..":
            self.__ListDBType()
            self.thisds = "/"
        elif self.thisds == "/":
            self.__ListDB(sel)
            self.thisds += "/"+sel
        else:
            try:
                dbcm = DBConfManager(self.thisds.split("/")[2])
                connstr = dbcm.GetConnectStr(sel)
                fds,rds,dirs = ListDBSysData(connstr)
                fds = [f.split(":")[-1] for f in fds]
                self.__ListDatas(fds,rds,dirs)
                self.thisds = "/"+connstr
            except:
                pass

    def __ListDatas(self, fds,rds,dirs):
        for tmpf in dirs:
            index = self.InsertImageStringItem(sys.maxint, tmpf,
                    self.imghs["dir"])
            self.SetStringItem(index,1,_('dir'))
        for tmpf in fds:
            index = self.InsertImageStringItem(sys.maxint, tmpf,
                    self.imghs["feature"])
            self.SetStringItem(index,1,_('feature'))
        for tmpf in rds:
            index = self.InsertImageStringItem(sys.maxint, tmpf,
                    self.imghs["raster"])
            self.SetStringItem(index,1,_('raster'))

    def __ListWebSystem(self):
        pass

    def GetSelected(self):
        return utf82locale(self.thisds[1:])

class DSListDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        wx.Dialog.__init__(self, *args, **kwds )
        self.dslist = DSListCtrl(self, -1,  style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.but = wx.Button(self,wx.ID_OK,_("OK"))
        self.butc = wx.Button(self,wx.ID_CANCEL,_("CANCEL"))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.dslist, 1, wx.EXPAND, 0)
        sizer_2.Add(wx.Panel(self, -1), 1, wx.EXPAND|wx.ALL, 5)
        sizer_2.Add(self.but, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        sizer_2.Add(self.butc, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.SetSize((300,400))
        self.Layout()
        wx.EVT_BUTTON( self, wx.ID_OK, self.OnOK)
        wx.EVT_BUTTON( self, wx.ID_CANCEL, self.OnCancel)

    def OnOK(self, evt):
        self.EndModal(wx.ID_OK)
        self.Destroy()
    def OnCancel(self, evt):
        self.EndModal(wx.ID_CANCEL)
        self.Destroy()
        
    def GetSelected(self):
        return self.dslist.GetSelected()

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.list_ctrl_1 = DSListCtrl(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.SetTitle("frame_1")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

if __name__ == "__main__":
    RunSysConf()
    app = MyApp(0)
    app.MainLoop()