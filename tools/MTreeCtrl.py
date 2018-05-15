#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx,os,copy,gettext,time

cat = gettext.GNUTranslations(open("lang/gb.mo",'rb'))
_ = cat.ugettext

PY_TEMPLATE = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
\"\"\"


 - writer:linux_23; create: %s ; version:1; 创建
\"\"\"

""" % time.ctime()

SYSNAME = os.name

import locale
syslocale = locale.getdefaultlocale()

def utf82locale(s):
    if type(s) == unicode:
        return s.encode(syslocale[1])
    return s.decode('utf-8').encode(syslocale[1])

class MListPanel(wx.Panel):
    def __init__(self, parent, infolist, fcfoo):
        wx.Panel.__init__(self, parent,-1)
        self.infolist = infolist
        self.fcfoo = fcfoo
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.list1 = wx.ListBox(self, -1)
        for i in infolist:
            self.list1.Append(i[0]+' {%d}' % i[1])
        sizer.Add(self.list1,1,wx.EXPAND,0)
        self.SetSizer(sizer)
        self.list1.Bind(wx.EVT_LISTBOX_DCLICK, self.lb1)
    def lb1(self,evt):
        index = evt.GetSelection()
        self.fcfoo(self.infolist[index][0], self.infolist[index][1])
        
class MListFrame(wx.Frame):
    def __init__(self,parent,infos, fcfoo):
        wx.Frame.__init__(self,parent,-1)
        self.panel = MListPanel(self,infos, fcfoo)

def walkfunc(iargs,thisdir,files):
    fstr = iargs[0]
    infos = iargs[1]
    dirlist = thisdir.split(os.path.sep)
    isrightdir = True
    for i in dirlist:
        if i.startswith('.'):
            isrightdir = False
            break
    if not isrightdir: return
    for f in files:
        if f.startswith('.') or f.endswith('~'):
            continue
        thispath = os.path.join(thisdir, f)
        if os.path.isfile(thispath):
            file = open(thispath)
            line = file.readline()
            iline = 1
            fstr = utf82locale(fstr)
            while(line):
                if fstr in line:
                    infos.append([thispath,iline])
                iline += 1
                line = file.readline()

            file.close()

def FindStrInFiles(inpath, fstr):
    infos = []
    os.path.walk(os.path.realpath(inpath),walkfunc,[fstr,infos])
    return infos


def RemoveDir(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

class MTreeCtrl(wx.TreeCtrl):
    def __init__(self, *args, **kwds):
        wx.TreeCtrl.__init__(self, *args, **kwds)
        #print dir(self)
        self.InitEnvVal()
        self.thisdir = os.getcwd()
        os.chdir('..')
        self.PROJHOME=os.getcwd()
        print self.PROJHOME
        self.root = self.AddRoot(_("ROOT"))
        self.__UpdateTree__()
        #print dir(self.root)
        self.Expand(self.root)

        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnDragBegin)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnItemRightClick)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
    def InitEnvVal(self):
        conffile = open("projctrl.conf")
        self.envval = {}
        for line in conffile.readlines():
            line = line.replace('\n','')
            line = line.replace('\r','')
            key_val = line.split("=")
            #print key_val
            if len(key_val)==2:
                self.envval[key_val[0]] = key_val[1]
            #print self.envval
        conffile.close()

    def __AddItem__(self,pathname,item):
        #walk = os.walk(pathname)
        self.__addi__(pathname,item)
        #self.SortChildren(item)
    def __addi__(self,pathname,item):
        #path,dirs,files = walk.next()
        ents = os.listdir(pathname)
        dirs = []
        files = []
        for i in ents:
            path = os.path.join(pathname,i)
            if os.path.isdir(path):
                dirs.append(i)
            if os.path.isfile(path):
                files.append(i)
        dirs.sort()#reverse=True)
        for d in dirs:
            if not d.startswith('.'):
                #print path,d
                i = self.AppendItem(item,d+'/')
                self.__addi__(os.path.join(pathname,d),i)

        files.sort()#reverse=True)
        for f in files:
            if not f.startswith('.') \
                and not f.endswith('~') \
                 and not f.endswith('.pyc'):
                self.AppendItem(item,f)
            

    def __UpdateTree__(self):
        self.DeleteChildren(self.root)
        self.__AddItem__(self.PROJHOME,self.root)
        self.Refresh()

    def OnDragBegin(self,evt):
        url = self.GetItemPath(evt.GetItem())
        data = wx.FileDataObject()
        data.AddFile(url)

        dropSource = wx.DropSource(self)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop()
        
    def OnItemRightClick(self,evt):
        itemid = self.GetSelection()
        isroot = self.IsRoot(itemid)
        if isroot:
            menu = self.GetRootMenu()
        else:
            if self.IsFile(itemid):
                menu = self.GetItemMenu()
            else:
                menu = self.GetDirMenu()
        if menu is not None:
            self.PopupMenu(menu,evt.GetPoint())
            menu.Destroy()

    def IsRoot(self,itemid):
        rootid = self.GetRootItem()
        return itemid == rootid

    def IsFile(self,itemid):
        text = self.GetItemText(itemid)
        if text.endswith("/"):
            return False
        else:  return True

    def GetItemMenu(self):
        menu = wx.Menu()
        menu.Append(1100, _("Open"),  _("Open with default way"))
        menu.Append(1107, _("Run with args"),  _("Run with args"))
        menu.Append(1101, _("Edit"),  _("Open with default editor"))
        menu.Append(1102, _("Delete"),  _("Delete it"))
        menu.AppendSeparator()
        menu.Append(1106, _("Export"),  _("Export the file to html format"))
        self.Bind(wx.EVT_MENU, self.OnPopupOpen, id=1100)
        self.Bind(wx.EVT_MENU, self.OnPopupEdit, id=1101)
        self.Bind(wx.EVT_MENU, self.OnPopupDelete, id=1102)
        self.Bind(wx.EVT_MENU, self.OnPopupOutput, id=1106)
        self.Bind(wx.EVT_MENU, self.OnPopupRunWA, id=1107)
        return menu

    def GetDirMenu(self):
        menu = wx.Menu()
        menu.Append(3101, _("console"),  _("console hear"))
        menu.Append(3105, _("Search"),  _("Search str in files"))
        menu.AppendSeparator()
        menu.Append(3102, _("Delete"),  _("Delete it"))
        menu.Append(3103, _("New file"), _("Create a new file"))
        menu.Append(3104, _("New dir"), _("Create a new dir"))
        menu.Append(3106, _("New python file"), _("Create a new python file"))
        self.Bind(wx.EVT_MENU, self.OnConsole, id=3101)
        self.Bind(wx.EVT_MENU, self.OnSearch, id=3105)
        self.Bind(wx.EVT_MENU, self.OnPopupDelete, id=3102)
        self.Bind(wx.EVT_MENU, self.OnPopupNewFile, id=3103)
        self.Bind(wx.EVT_MENU, self.OnPopupNewPyFile, id=3106)
        self.Bind(wx.EVT_MENU, self.OnPopupNewDir, id=3104)
        return menu
    
    def GetRootMenu(self):
        menu = wx.Menu()
        menu.Append(3101, _("console"),  _("console hear"))
        menu.AppendSeparator()
        menu.Append(2100, _("ReFresh"),_("Export the file to html format"))
        menu.Append(3103, _("New file"), _("Create a new file"))
        menu.Append(3104, _("New dir"), _("Create a new dir"))
        self.Bind(wx.EVT_MENU, self.OnConsole, id=3101)
        self.Bind(wx.EVT_MENU, self.OnPopupReflush, id=2100)
        self.Bind(wx.EVT_MENU, self.OnPopupNewFile, id=3103)
        self.Bind(wx.EVT_MENU, self.OnPopupNewDir, id=3104)
        return menu

    def OnSearch(self, evt):
        path = self.GetItemPath(self.GetSelection())
        dlg = wx.TextEntryDialog(
                self, _('Input'), _("Enter the string to search"))
        if dlg.ShowModal() == wx.ID_OK:
            sstr = dlg.GetValue()
            infos = FindStrInFiles(path,sstr)
            listdlg = MListFrame(self,infos, self.OpenFileToN)
            listdlg.Show()

    def OpenFileToN(self,filepath, n):
        editorname = self.envval["DEF_EDITOR_N"]
        #print editorname, n, filepath
        comm = editorname % (n,filepath)
        if SYSNAME=="nt":
            newpid = self.envval['NEW_PID']
            if newpid == 'y':
                common = "start "+comm
            else:
                common = comm
        else:
            common = comm + " &"
        os.popen(common)

    def OnConsole(self,evt):
        try:
            path = self.GetItemPath(self.GetSelection())
        except:
            path = self.PROJHOME
        os.chdir(path)
        if os.name == 'nt':
            os.system('start cmd')
        else:
            os.system('xterm &')

    def OnPopupReflush(self,evt):
        self.__UpdateTree__()

    def OnPopupEdit(self,evt):
        filepath = self.GetItemPath(self.GetSelection())
        self.OnEdit(filepath)

    def OnEdit(self,filepath):
        editorname = self.envval["DEF_EDITOR"]
        if SYSNAME=="nt":
            newpid = self.envval['NEW_PID']
            if newpid == 'y':
                common = " ".join(["start",editorname,filepath])
            else:
                common = " ".join([editorname,filepath])
        else:
            common = " ".join([editorname,filepath,"&"])
        #print common
        #os.system(common)
        os.popen(common)

    def OnLeftDClick(self,evt):
        filepath = self.GetItemPath(self.GetSelection())
        if os.path.isfile(filepath):
            self.OnEdit(filepath)
        evt.Skip()

    def OnPopupOpen(self,evt):
        nowdir = os.getcwd()
        filepath = self.GetItemPath(self.GetSelection())
        ndir,npath = os.path.split(filepath)
        print filepath
        os.chdir(ndir)
        os.popen("start "+npath)
        os.chdir(nowdir)

    def OnPopupRunWA(self,evt):
        dlg = wx.TextEntryDialog(
                self, _('Input'), _("Enter the args for run"), _('args'))
        if dlg.ShowModal() == wx.ID_OK:
            args = dlg.GetValue()
            nowdir = os.getcwd()
            filepath = self.GetItemPath(self.GetSelection())
            ndir,npath = os.path.split(filepath)
            print filepath
            os.chdir(ndir)
            os.popen("start "+npath+" "+args)
            os.chdir(nowdir)

    def OnPopupNewFile(self,evt):
        try:
            path = self.GetItemPath(self.GetSelection())
        except:
            path = self.PROJHOME
        dlg = wx.TextEntryDialog(
                self, _('Input'), _("Enter the new file's name"), _('NewFile'))
        if dlg.ShowModal() == wx.ID_OK:
            allfile = os.listdir(path)
            filename = dlg.GetValue()
            if filename in allfile:
                wx.MessageBox(_("There already is a file named %s") % filename,_("error"))
            else:
                try:
                    file = open(os.path.join(path,dlg.GetValue()),'w')
                    file.close()
                    self.__UpdateTree__()
                except:
                    wx.MessageBox(_("new failed"),_("error"))
        dlg.Destroy()

    def OnPopupNewPyFile(self,evt):
        try:
            path = self.GetItemPath(self.GetSelection())
        except:
            path = self.PROJHOME
        dlg = wx.TextEntryDialog(
                self, _('Input'), _("Enter the new file's name"), _('NewFile'))
        if dlg.ShowModal() == wx.ID_OK:
            allfile = os.listdir(path)
            filename = dlg.GetValue()
            if filename in allfile:
                wx.MessageBox(_("There already is a file named %s") % filename,_("error"))
            else:
                try:
                    file = open(os.path.join(path,dlg.GetValue()),'w')
                    file.write(PY_TEMPLATE)
                    file.close()
                    self.__UpdateTree__()
                except:
                    wx.MessageBox(_("new failed"),_("error"))
        dlg.Destroy()

    def OnPopupNewDir(self,evt):
        try:
            path = self.GetItemPath(self.GetSelection())
        except:
            path = self.PROJHOME
        dlg = wx.TextEntryDialog(
                self, _('Input'), _("Enter the new folder's name"), _('NewFolder'))
        if dlg.ShowModal() == wx.ID_OK:
            allfile = os.listdir(path)
            filename = dlg.GetValue()
            if filename in allfile:
                wx.MessageBox(_("There already is a folder named %s") % filename,_("error"))
            else:
                try:
                    os.makedirs(os.path.join(path,dlg.GetValue()))
                    self.__UpdateTree__()
                except:
                    wx.MessageBox(_("new failed"),_("error"))
        dlg.Destroy()

    def OnPopupDelete(self,evt):
        yn = wx.MessageBox(_("delete? This is dangerous !"),
                _('dangerous!!'),wx.YES_NO)
        if yn==wx.YES:
            path = self.GetItemPath(self.GetSelection())
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    RemoveDir(path)
                    os.rmdir(path)
            except:
                wx.MessageBox(_("delete failed"),_("error"))
            self.__UpdateTree__()

    def OnPopupOutput(self,evt):
        pass

    def GetItemPath(self,itemid):
        pathstr = [self.GetItemText(itemid)]
        rootid = self.GetRootItem()
        thisitemid = self.GetItemParent(itemid)
        while thisitemid != rootid:
            pathstr.insert(0,self.GetItemText(thisitemid)[:-1])
            thisitemid = self.GetItemParent(thisitemid)
        pathstr.insert(0,self.PROJHOME)
        if SYSNAME=='nt':
            return "\\".join(pathstr)
        else:
            return "/".join(pathstr)
