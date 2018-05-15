# -*- encoding:utf-8 -*-
"""进行Log输出的控件

 - writer:linux_23; create: 2008.4.8; version:1; 创建

"""
import wx, logging

from geosings.core.system.EncodeTran import *
from geosings.core.system.GLog import *

class wxLogHandler(logging.Handler):
    """
    界面的log操作Handler
    """
    def __init__(self, uictrl):
        logging.Handler.__init__(self)
        self.ui = uictrl
        self.levelcolor = [
            wx.TextAttr("GRAY", wx.NullColour),#DEBUG
            wx.TextAttr("BLACK", wx.NullColour),#INFO
            wx.TextAttr("ORANGE", wx.NullColour),#WARNING
            wx.TextAttr("RED", wx.NullColour),#ERROR
            wx.TextAttr("PINK", wx.NullColour),#CRITICAL
            wx.TextAttr("BLUE", wx.NullColour),#ORDER
        ]
    def flush(self):
        pass
    def emit(self, record):
        """
        处理一个记录
        """
        try:
            msg = self.format(record)
            fs = "%s\n"
            i = 1
            levelcolor = self.levelcolor[-1]
            for color in self.levelcolor:
                if record.levelno<10*(i+1):
                    levelcolor = color
                    break
                i+=1
            self.ui.SetDefaultStyle(levelcolor)
            #if not hasattr(types, "UnicodeType"): #if no unicode support...
            #    self.ui.AppendText(fs % msg)
            #else:
            #    try:
            #        self.ui.AppendText(fs % msg)
            #    except UnicodeError:
            #        self.ui.AppendText(fs % msg.encode("UTF-8"))
            self.ui.AppendText(fs % any2utf8(msg))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

class LogTextCtrl(wx.TextCtrl):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL|wx.TE_MULTILINE|wx.TE_RICH2
        wx.TextCtrl.__init__(self, *args, **kwds)
        self.logh = wxLogHandler(self)
        register_log_handler(self.logh, logging.DEBUG)

if __name__=="__main__":
    #测试
    class TestOutputPanel(wx.Panel):
        def __init__(self, *args, **kwds):
            kwds["style"] = wx.TAB_TRAVERSAL
            wx.Panel.__init__(self, *args, **kwds)
            self.text_ctrl_1 = LogTextCtrl(self, -1, "")
            self.__do_layout()

            for i in range(2):
                info("#"*30)
                debug(u"debug测试 %d",i)
                warning("测试warning %d",i)
                error("错误！！！！！")
                order("open file %d" % i)

        def __do_layout(self):
            sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_2 = wx.BoxSizer(wx.VERTICAL)
            sizer_1.Add(self.text_ctrl_1, 1, wx.EXPAND,2)
            self.SetAutoLayout(True)
            sizer_2.Add(sizer_1, 1, wx.EXPAND, 2)
            self.SetSizer(sizer_2)
            sizer_2.Fit(self)
            sizer_2.SetSizeHints(self)

    from geosings.ui.commondlg.TestFrame import RunTest
    RunTest(TestOutputPanel, -1)

