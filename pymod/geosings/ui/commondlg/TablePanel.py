# -*- coding: utf-8 -*-
"""
定义一个表控件
"""
import wx
import sys

class MyTable(wx.ListCtrl):
    """表控件
    """
    def __init__(self,parent,id):
        """初始化表控件
        @type parent: wxCtrl
        @param parent: 父控件
        @type id: int
        @param id: 控件id
        """
        wx.ListCtrl.__init__(self,parent,id,
                 style=wx.LC_REPORT 
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 | wx.LC_VIRTUAL
                                 #| wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 | wx.LC_VRULES
                                 | wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
    
    def OnGetItemText(self, item, col):
        """设置Item的值，这是一个wxListCtrl挂钩函数
        @type item: int
        @param item: 项所处的行
        @type col: int
        @param col: 项所处的列
        @rtype: str
        @return: 项的值
        """
        return self.vals[item][col]

    def InitColumns(self,cols):
        """初始化列集合
        @type cols: list
        @param cols: 列的名字集合
        """
        self.cols = cols
        self.colcount = len(cols)
        for i in range(self.colcount):
            self.InsertColumn(i,cols[i])

    def InitItems(self,vals):
        """初始化项
        @type vals: list
        @param vals: 设置项的值
        """
        self.vals = vals
        self.SetItemCount(len(vals))

class TablePanel(wx.Panel):
    """表控件所在的面板
    """
    def __init__(self,parent):
        """初始化表的面板
        @type parent: wxCtrl
        @param parent: 父控件
        """
        wx.Panel.__init__(self,parent,-1)

        self.list = MyTable(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list,1,wx.EXPAND,0)
        self.SetSizer(sizer)
        
    def InitColumns(self,cols):
        """初始化所有的列的列表
        @type cols: list
        @param cols: 初始化列的名称列表
        """
        self.list.InitColumns(cols)

    def InitItems(self,vals):
        """初始化所有值的列表
        @type vals: list
        @param vals: 插入所有的数值
        """
        self.list.InitItems(vals)

    def SetData(self,cols,vals):
        """设置所有表内容（包括列和值）
        @type cols: list
        @param cols: 列的值的列表
        @type vals: list
        @param vals: 表的所有值
        """
        self.InitColumns(cols)
        self.InitItems(vals)

    def ClearAll(self):
        """清楚所有的内容
        """
        self.list.ClearAll()


class TableFrame(wx.Frame):
    """放表面板的框架
    """
    def __init__(self,parent):
        """初始化框架
        @type parent: wxCtrl
        @param parent: 父控件
        """
        wx.Frame.__init__(self,parent,-1)
        self.panel = TablePanel(self)

    def SetData(self,cols,vals):
        """设置内容
        @type cols: list
        @param cols: 列的名称列表
        @type vals: list
        @param vals: 列的值列表
        """
        self.panel.InitColumns(cols)
        self.panel.InitItems(vals)


if __name__ == '__main__':
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = TableFrame(None)
    app.SetTopWindow(frame_1)
    cols = ['asdf','qwre']
    #vals = [['asfdinsadfn','qrwe'],
    #            ['1','3']
    #            ]
    import time
    beg = time.time()
    vals = [(str(i),str(i+1)) for i in range(16000)]
    print time.time()-beg
    beg = time.time()
    frame_1.SetData(cols,vals)
    print time.time()-beg
    ret = frame_1.Show()
    app.MainLoop()
