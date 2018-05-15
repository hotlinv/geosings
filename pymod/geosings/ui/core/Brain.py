# -*- coding: utf-8 -*-
"""
该模块是进行消息的解析和分发,相当于人体的大脑
"""


#from UISettings import *
from UIConst import ActionResult
from Document import mainDocument
from geosings.core.system.GLog import *
from geosings.core.Exception import *

class MsgParser:
    """消息的分析处理类
    """
    def __init__(self):
        """构造函数
        """
        #self.uictrl = None
        pass

    def SendMsg(self,msg):
        """发送消息
        @type msg: str
        @param msg: 要发送的消息
        """
        from geosings.core.system.GssConfDict import GSSMSGS,GSSCONF
        info( _('message')+':\"%s\"',msg)
        self.msg = msg
        self.msgs = msg.split()
        self.order = self.msgs[0]
        MsgKeyMap = GSSCONF["MSGKEY"].GetKeyMap()
        function = MsgKeyMap.get(self.order,None)
        if function is not None:
            if len(self.msgs) > 1:
                self.result = function(" ".join(self.msgs[1:len(self.msgs)]))
            else:
                self.result = function()
            debug(_("action end"))
        else:
            debug("have no operator named %s",self.order)
            #mainDocument.ErrNo = ErrorNum.NoOrderErr
            self.result = ActionResult.Failuse 
            raise NoOrderException()

    

msgParser = MsgParser()
