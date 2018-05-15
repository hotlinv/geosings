# -*- coding: utf-8 -*-
"""该模块是进行OpenGL的离屏渲染环境的构建
已经废弃
"""

import os
import Image,Numeric

if os.name == 'nt':
    # windows系统
    import _wglContext
    __SaveBmp = _wglContext.SaveBmp
    __SaveBmp2 = _wglContext.SaveBmp2
    
    StartGLContext = _wglContext.StartBmpContext
    """初始化OpenGL的离屏渲染环境
    """
    
    GetMemData = _wglContext.GetMemBmpData
    """获取渲染后的数据
        - 返回渲染后图像的二进制数据
    """

    EndGLContext = _wglContext.EndBmpContext
    """关闭离屏渲染环境
    """

    GetGLCanvasWidth = _wglContext.GetWidth
    """获取GL的渲染宽度
        - 返回渲染宽度
    """

    GetGLCanvasHeight = _wglContext.GetHeight
    """获取GL的渲染高度
        - 返回渲染高度
    """
else:
    #posix系统,X桌面环境
    import _glXContext
    StartGLContext = _glXContext.StartGLXContext
    """初始化OpenGL的离屏渲染环境
    """
    EndGLContext = _glXContext.EndGLXContext
    """关闭离屏渲染环境
    """
    GetMemData = _glXContext.GetMemData
    """获取渲染后的数据
        - 返回渲染后图像的二进制数据
    """
    GetGLCanvasWidth = _glXContext.GetWidth
    """获取GL的渲染宽度
        - 返回渲染宽度
    """

    GetGLCanvasHeight = _glXContext.GetHeight
    """获取GL的渲染高度
        - 返回渲染高度
    """



_enable = 0
"""环境是否可用
"""

class glOffScreenRC:
    """对OpenGL的离屏渲染RC环境进行包装
    """
    def __init__(self, w, h):
        """初始化GL的环境
        @type w: int
        @param w: 离屏渲染的画布宽
        @type h: int
        @param h: 离屏渲染的画布高
        """
        global _enable
        if _enable == 0:
            StartGLContext(w,h)
            _enable = 1
        else:
            EndGLContext()
            StartGLContext(w,h)
            _enable = 1

    def __del__(self):
        """析构环境
        """
        self.Destroy()

    def GetGLCanvasWidth(self):
        """获取GL的画布宽
        @rtype: int
        @return: 返回GL的画布宽
        """
        return GetGLCanvasWidth()

    def GetGLCanvasHeight(self):
        """获取GL的画布高
        @rtype: int
        @return: 返回GL的画布高
        """
        return GetGLCanvasHeight()

    def GetMemData(self):
        """获取数据
        @rtype: str
        @return: 返回二进制数据
        """
        return GetMemData()

    def Destroy(self):
        """销毁GL的画布
        """
        global _enable
        if _enable == 1:
            EndGLContext()
            _enable = 0

    def Output(self, path, type):
        """输出成图片
        @type path: str
        @param path: 输出图片的位置
        @type type: str
        @param path: 输出图片的类型，比如png，jpg等等
        """
        data  = self.GetMemData()
        arr = Numeric.fromstring(data,Numeric.Int8)
        arr.shape = (-1,4)
        arr = arr[:,0:3]
        of = path

        img = Image.fromstring("RGB", \
                (self.GetGLCanvasWidth(),self.GetGLCanvasHeight()) \
                ,arr.tostring()) \
                .transpose(Image.FLIP_TOP_BOTTOM) \
                .save(of,type)

