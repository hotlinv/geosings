# -*- coding: utf-8 -*-
"""
该模块定义注记有关类和方法

 - writer:linux_23; create:2007.5.29; version:1; 创建
"""

from Symbol import GetDefTextSymbol,TextSymConfKeys

class AnnotateProps:
    """标注设置参数
    """
    def __init__(self,confmap={}):
        """构造函数
        @type confmap: map
        @param confmap: 配置字典
        """
        self.field = 'name' #要显示的域的名字
        self.symbol = GetDefTextSymbol() #标注样式

        if 'field' in confmap:#如果用户指定特定field
            self.field = confmap['field']
        
        for key in TextSymConfKeys:
            if key in confmap:#用户指定文字标注类型
                self.symbol[key] = confmap[key]
