# -*- coding: utf-8 -*-
"""该模块定义选择路径对话框
"""

import wx, os, re
from geosings.core.gssconst import VDSFormatMap, RDSFormatMap, DSFormatMap
from geosings.core.system.DefConf import USERHOME
from geosings.core.system.EncodeTran import utf82locale
from geosings.core.system.GssConfDict import GSSCONF
from geosings.core.DataSet import DBConfManager, ListDBSysData
from geosings.core.system import SaveUtf8File, OpenUtf8

allcard = "|All files (*.*)|*.*"

def getWildcard(fileext):
    """根据扩展名写出过滤字符串
    """
    extarr = fileext.split('/')
    exts = ";".join(["*.%s" % i for i in extarr])
    extstr = "("+";".join(["*.%s" % i for i in extarr])+")"
    card = "|".join([extstr,exts])#+allcard
    return card

class DBEditDlg(wx.Dialog):
    def __init__(self,parent,name,dbconf):
        wx.Dialog.__init__(self,parent,-1)
        self.dbconf = dbconf
        self.name = name
        infos = self.dbconf.GetInfos(name)
        l0 = wx.StaticText(self,-1,_("name"))
        self.ed_name = wx.TextCtrl(self,-1,name)
        l1 = wx.StaticText(self,-1,_("host"))
        self.ed_host = wx.TextCtrl(self,-1,infos["host"])
        l2 = wx.StaticText(self,-1,_("dbname"))
        self.ed_dbname = wx.TextCtrl(self,-1,infos["dbname"])
        l3 = wx.StaticText(self,-1,_("user"))
        self.ed_user = wx.TextCtrl(self,-1,infos["user"])
        l4 = wx.StaticText(self,-1,_("password"))
        self.ed_pwd = wx.TextCtrl(self,-1,infos["password"])

        self.but_ok = wx.Button(self,wx.ID_OK,_("OK"))
        self.but_cancel = wx.Button(self,wx.ID_CANCEL,_("Cancel"))

        sizer = wx.FlexGridSizer(cols=3, hgap=4, vgap=4)
        sizer.AddMany([ l0, self.ed_name, (0,0),
                        l1, self.ed_host, (0,0),
                        l2, self.ed_dbname, (0,0),
                        l3, self.ed_user, (0,0),
                        l4, self.ed_pwd, (0,0),
                        (0,0), self.but_ok, self.but_cancel,
                        ])

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.but_ok.Bind(wx.EVT_BUTTON, self.OnOK)
        self.but_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)

    def OnOK(self,evt):
        try:
            if self.name=="":
                self.dbconf.Add(self.ed_name.GetValue(),
                        self.ed_host.GetValue(),
                        self.ed_dbname.GetValue(),
                        self.ed_user.GetValue(),
                        self.ed_pwd.GetValue())
            else:
                self.dbconf.Edit(self.ed_name.GetValue(),
                        self.ed_host.GetValue(),
                        self.ed_dbname.GetValue(),
                        self.ed_user.GetValue(),
                        self.ed_pwd.GetValue())
        except:
            wx.MessageBox(_("same name"))
        evt.Skip()

    def OnCancel(self,evt):
        pass
        evt.Skip()

    def LoadConf(self,name):
        if name in self.dbconf.GetDBList():
            pass
            
        
class DBOpenDlg(wx.Dialog):
    def __init__(self,parent,dbtype):
        wx.Dialog.__init__(self,parent,-1)
        self.conn = ""
        self.dbtype = dbtype
        self.dbconf = DBConfManager(dbtype)
        self.listbox = wx.ListBox(self,-1)
        dblist = self.dbconf.GetDBList()
        for dbi in dblist: self.listbox.Append(dbi)
        self.butadd = wx.Button(self,-1,_("Add"))
        self.butedit = wx.Button(self,-1,_("Edit"))
        self.butdel = wx.Button(self,-1,_("Delete"))
        self.butok = wx.Button(self,wx.ID_OK,_("OK"))
        self.butcancel = wx.Button(self,wx.ID_CANCEL,_("Cancel"))
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.listbox, 1, wx.EXPAND|wx.ALL ,5)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.butadd)
        sizer2.Add(self.butedit)
        sizer2.Add(self.butdel)
        sizer2.Add(self.butok)
        sizer2.Add(self.butcancel)
        sizer1.Add(sizer2,0,wx.ALIGN_CENTER|wx.ALL, 5)
        
        self.SetSizer(sizer1)
        self.SetSize((500,400))
        self.SetAutoLayout(True)
        self.Layout()

        self.butadd.Bind(wx.EVT_BUTTON, self.AddConf)
        self.butdel.Bind(wx.EVT_BUTTON, self.DeleteConf)
        self.butedit.Bind(wx.EVT_BUTTON, self.EditConf)
        self.butok.Bind(wx.EVT_BUTTON, self.OnOK)

    def OnOK(self,evt):
        name = self.listbox.GetStringSelection()
        self.conn = self.dbconf.GetConnectStr(name)

        evt.Skip()

    def AddConf(self,evt):
        dlg = DBEditDlg(self,"",self.dbconf)
        dlg.ShowModal()
        dlg.Destroy()
        self.listbox.Clear()
        dslist = self.dbconf.GetDBList()
        for i in dslist:
            self.listbox.Append(i)
        self.listbox.SetSelection(0)
    
    def EditConf(self,evt):
        name = self.listbox.GetStringSelection()
        dlg = DBEditDlg(self,name,self.dbconf)
        dlg.ShowModal()
        dlg.Destroy()

    def DeleteConf(self,evt):
        sel = self.listbox.GetStringSelection()
        self.dbconf.Delete(sel)
        self.listbox.Clear()
        dslist = self.dbconf.GetDBList()
        for i in dslist:
            self.listbox.Append(i)
        self.listbox.SetSelection(0)

    def GetConnect(self):
        return self.conn
    
class OpenLayerDlg(wx.Dialog):
    """路径选择对话框
    """
    def __init__(self,parent,vra='a'):
        """初始化对话框
        @type parent: wxCtrl
        @param parent: 父框架
        """
        wx.Dialog.__init__(self,parent,-1)
        self.path = ""
        if vra == 'v':
            self.FormatMap = VDSFormatMap
        elif vra == 'r':
            self.FormatMap = RDSFormatMap
        else:
            self.FormatMap = DSFormatMap
        self.format = self.FormatMap.keys()[0]

        self.formatlist = wx.ListBox(self, -1, size = (100,200), choices = self.FormatMap.keys())
        self.formatlist.SetSelection(0)
        self.dslist = wx.ListBox(self, -1, size = (-1,200), style=wx.LB_HSCROLL )
        self.tesource = wx.TextCtrl(self, -1, "", size=(-1,20))
        self.butsource = wx.Button(self,1,_("DataSource"))
        self.but = wx.Button(self,wx.ID_OK,_("OK"))
        self.butc = wx.Button(self,wx.ID_CANCEL,_("Cancel"))

        sz = wx.BoxSizer(wx.HORIZONTAL)
        sz2 = wx.BoxSizer(wx.VERTICAL)
        szSource = wx.BoxSizer(wx.HORIZONTAL)
        szBut = wx.BoxSizer(wx.HORIZONTAL)

        sz.Add(self.formatlist, 0, wx.EXPAND|wx.ALL,5)

        #sz.Add((35,35))

        sz.Add(sz2, 1, wx.EXPAND|wx.ALL, 0)

        sz2.Add(szSource, 0, wx.ALL|wx.EXPAND, 5)
        sz2.Add(self.dslist, 1, wx.ALL|wx.EXPAND, 5)
        sz2.Add(szBut, 0, wx.ALL|wx.EXPAND, 5)

        szSource.Add(self.tesource, 1, wx.ALL|wx.EXPAND, 0)
        szSource.Add((5,5))
        szSource.Add(self.butsource, 0, wx.ALL, 0)

        szBut.Add(wx.Panel(self,-1), 1, wx.EXPAND|wx.ALL, 0)
        szBut.Add(self.but, 0, wx.ALL, 0)
        szBut.Add(self.butc, 0, wx.ALL, 0)

        self.SetSizer(sz)
        self.SetSize((500,400))
        self.SetAutoLayout(True)
        self.Layout()

        #self.but.Bind(wx.EVT_BUTTON, self.OnSel)
        self.formatlist.Bind(wx.EVT_LISTBOX, self.OnSelFormat)
        self.butsource.Bind(wx.EVT_BUTTON, self.OnOpenDataSource)
        #wx.EVT_BUTTON( self, wx.ID_OK, self.OnSel)
   
    def OnSelFormat(self, evt):
        self.format = evt.GetString()
    
    def OnOpenDataSource(self, evt):
        gdalinfo = GSSCONF["GDALINFO_APP"]
        ogrinfo = GSSCONF["OGRINFO_APP"]
        if self.format == "PostgreSQL" or \
                self.format == "MySQL":#数据库型数据源
            dlg = DBOpenDlg(self, self.format)
            if dlg.ShowModal() == wx.ID_OK:
                conn = dlg.GetConnect()
                print "conn",conn
                self.tesource.SetValue(conn)
                self.dslist.Clear()

                subnames = ListDBSysData(conn)[0]

                for i in subnames: self.dslist.Append(i)
                try:
                    self.dslist.SetSelection(0)
                except:#选择错误则略过
                    pass
        else:
            #elif self.format == "GeoTIFF" or \
                    #   self.format == "Shape file" or \
                    #   self.format == "Mapinfo file" or \
                    #   self.format == "hdf4/hdf5":#文件型数据源
            opath = os.path.join( USERHOME, ".lastfpath" )
            if not os.access(opath,os.F_OK):SaveUtf8File(opath,u'')
            f = OpenUtf8(opath,'r')
            line = f.readline().strip()
            if line=='': line = os.getcwd()
            dlg = wx.FileDialog(
                None, message="Open File as ...", defaultDir=line, 
                defaultFile="", wildcard=getWildcard(self.FormatMap[self.format]), style=wx.OPEN
                )
            f.close()
            if dlg.ShowModal()==wx.ID_OK:
                path = dlg.GetPath()
                pp = os.path.split(path)[0]
                SaveUtf8File(opath, pp)
                if self.format == "hdf4/hdf5":
                    self.tesource.SetValue(path)
                    self.dslist.Clear()
                    #opath = os.path.join( USERHOME, ".hdfinfo" )
                    #os.system(" ".join(["gdalinfo",path,">",'"'+opath+'"']))
                    hdfinfof = os.popen('%s "%s"' % (gdalinfo, path))#open(opath,'r')
                    subnames = []
                    restr = r"^SUBDATASET_\d+_NAME=(.+)$"
                    line = hdfinfof.readline().strip()
                    while line: 
                        #print line
                        m = re.match(restr, line)
                        if m is not None:
                            #print m.groups()
                            gs = m.groups()
                            subnames.append(gs[0])
                        line = hdfinfof.readline().strip()
                    for i in subnames: self.dslist.Append(i)
                    self.dslist.SetSelection(0)
                    hdfinfof.close()
                else:
                    self.tesource.SetValue(path)
                    self.dslist.Clear()
                    self.dslist.Append(path)
                    self.dslist.SetSelection(0)
            #else:
            #    self.path = ""

    def GetPath(self):
        """获取选择的路径
        @rtype: str
        @return: 路径
        """
        return utf82locale(self.dslist.GetStringSelection())
        #return self.path
        
def testApp():
    """测试
    """
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = OpenLayerDlg(None)
    app.SetTopWindow(frame_1)
    frame_1.ShowModal()
    print frame_1.GetPath()

if __name__ == "__main__":
    testApp()
