# -*- coding: utf-8 -*-
"""
该模块定义图层信息输出面板
"""
import wx
import wx.html as html
import os

class MyHtmlWindow(html.HtmlWindow):
    """图层信息输出窗口
    """
    def __init__(self,parent,id):
        """初始化窗口
        @type parent: wxCtrl
        @param parent: 父窗口
        @type id: int
        @param id: 该窗口的id
        """
        html.HtmlWindow.__init__(self,parent,id)
        #thispath = os.path.realpath("..")
        #self.LoadPage("../../../docs/index.html")

class HtmlFrame(wx.Frame):
    """图层信息的框架
    """
    def __init__(self,*args,**kwds):
        """初始化框架
        """
        wx.Frame.__init__(self,*args,**kwds)
        self.panel = MyHtmlWindow(self,1)
        sizermain = wx.BoxSizer(wx.VERTICAL)
        sizermain.Add(self.panel, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizermain)
        self.SetSize((540,650))
        self.Layout()

    def LoadPage(self,url):
        """加载页面
        @type url: str
        @param url: 页面的url
        """
        self.panel.LoadPage(url)

    def LoadFile(self,url):
        """加载文件
        @type url: str
        @param url: 文件的地址
        """
        self.panel.LoadFile(url)

    def LoadString(self,string):
        """加载html字符串
        @type string: str
        @param string: html的字符串内容
        """
        print string
        self.panel.SetPage(string)

def run(url = None):
    """运行主面板
    """
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    mainframe = HtmlFrame(None, -1, "")
    app.SetTopWindow(mainframe)
    if url is not None:
        mainframe.LoadFile(url)
        #print dir(mainframe.panel)
    mainframe.Show()
    app.MainLoop()

if __name__ == "__main__":
    from geosings.core.DefConf import DOCHOME
    run(DOCHOME+'/index.html')

