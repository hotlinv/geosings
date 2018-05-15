# -*- coding: utf-8 -*-
"""
该模块定义数据列表管理界面(已经作废,被MyMTreePanel代替)
"""

import wx
from Document import *

class DataListCtrl(wx.TreeCtrl):
    """数据列表管理控件
    """
    def __init__(self,parent,mainctrl):
        """初始化控件，绑定处理消息函数
        @type parent: wxCtrl
        @param parent: 所属的父控件
        @type mainctrl: wxCtrl
        @param mainctrl: 实际操作数据的控件
        """
        wx.TreeCtrl.__init__(self,parent,-1,
                style=wx.TR_MULTIPLE
                     |wx.TR_FULL_ROW_HIGHLIGHT
                      )
        self.mainctrl = mainctrl
        self.root = self.AddRoot("DataSets")
        #self.but = TreeButton(self)
        
        self.Bind(wx.EVT_CHAR, self.OnChar)
        self.Bind(wx.EVT_TREE_SEL_CHANGING,self.OnSelectedItem)
        self.Bind(wx.EVT_TREE_GET_INFO,self.OnLeftDown)
        #self.Bind(wx.EVT_LEFT_DOWN,self.OnLeftDown)

    def OnLeftDown(self,evt):
        """左键按下后的操作
        @type evt: wxEvent
        @param evt: wx的鼠标事件
        """
        print 'leftdown'
        self.SelectLayer()

    def OnSelectedItem(self,evt):
        """在树控件改变选择后执行的操作
        @type evt: wxEvent
        @param evt: wx的EVT_TREE_SEL_CHANGING事件
        """
        self.SelectLayer()

    def SelectLayer(self):
        """选择图层
        """
        i = self.GetChildrenCount(self.root)
        #sels = self.GetSelections()
        #sels = [sel[0] for sel in sels]
        nowid,cookie = self.GetFirstChild(self.root)
        items = []
        while ( i!=0) :
            #if (nowid in sels):
            if (self.IsSelected(nowid)) :
                items.append(i-1)
            i-=1
            nowid,cookie = self.GetNextChild(nowid,cookie)
        mainDocument.SelectedLayer(items)
    def OnChar(self, evt):
        """在树控件键盘输入时的相应
        @type evt: wxEvent
        @param evt: wx的EVT_CHAR事件
        """
        self.mainctrl.EvtOrder(evt) 

    def AddDataSet(self,name,type='',visual=1):
        """添加数据集
        @type name: str
        @param name: 数据集的名称
        @type type: str
        @param type: 数据集的类型
        @type visual: bool
        @param visual: 数据集可见与否
        """
        if visual:
            self.InsertItemBefore(self.root, 0, \
                    '* %s (%s)' % (name,type))
        else:
            self.InsertItemBefore(self.root, 0, \
                    '  %s (%s)' % (name,type))

    def RemoveDataSet(self,index):
        """移除数据集
        @type index: int
        @param index: 要移除数据集的索引
        """
        pass

    def UpdateAll(self):
        """更新所有的数据集列表
        """
        self.DeleteChildren(self.root)
        for ds in mainDocument.layers:
            if ds is not None:
                self.AddDataSet(ds.name,ds.GetTypeName(),ds.visual)
        self.Expand(self.root)
        self.Refresh()
