# -*- coding: utf-8 -*-

from ctypes import *
from OpenGL.GL import *
import Numeric, Image

#定义GLX常数
GLX_RGBA = 4
GLX_RED_SIZE = 8
GLX_GREEN_SIZE = 9
GLX_BLUE_SIZE = 10

class XVisualInfo(Structure):
    """定义XVisualInfo的结构体
    """
    _fields_ = [("visual", c_void_p),
                ("visualid", c_uint),
                ("screen", c_int),
                ("depth", c_uint),
                ("class", c_int),
                ("red_mask", c_ulong),
                ("green_mask", c_ulong),
                ("blue_mask", c_ulong),
                ("colormap_size", c_int),
                ("bits_per_rgb", c_int),
                ]


class glXOffScreenRC:
    """对OpenGL的离屏渲染RC环境进行包装
    """
    def __init__(self, w, h):
        """初始化GL的环境
        @type w: int
        @param w: 离屏渲染的画布宽
        @type h: int
        @param h: 离屏渲染的画布高
        """
        self.enable = False
        self.w = w
        self.h = h
        self.GL = CDLL('libGL.so.1')
        self.X11 = CDLL('libX11.so.6')
        GL,X11 = self.GL,self.X11

        self.dpy = X11.XOpenDisplay(0)

        sbAttrib = (c_int*8)(GLX_RGBA,
                        GLX_RED_SIZE,1,
                        GLX_GREEN_SIZE,1,
                        GLX_BLUE_SIZE,1,
                        0)

        scrnum = X11.XDefaultScreen(self.dpy)
        root = X11.XRootWindow(self.dpy,scrnum)
        GL.glXChooseVisual.restype = POINTER(XVisualInfo)
        visinfo = GL.glXChooseVisual( self.dpy, scrnum, sbAttrib )
        self.ctx = GL.glXCreateContext( self.dpy, visinfo, 0, False )
        self.pm = X11.XCreatePixmap( self.dpy, root, self.w, self.h, visinfo.contents.depth );
        self.glxpm = GL.glXCreateGLXPixmap( self.dpy, visinfo, self.pm );
        GL.glXMakeCurrent( self.dpy, self.glxpm, self.ctx );
        self.enable = True

    def Destroy(self):
        """销毁GL的画布
        """
        GL,X11 = self.GL,self.X11
        GL.glXDestroyGLXPixmap(self.dpy,self.glxpm);
        X11.XFreePixmap(self.dpy,self.pm);
        GL.glXDestroyContext(self.dpy,self.ctx);
        self.enable = False

    def __del__(self):
        """析构环境
        """
        if self.enable:
            self.Destroy()

    def GetGLCanvasWidth(self):
        """获取GL的画布宽
        @rtype: int
        @return: 返回GL的画布宽
        """
        return self.w

    def GetGLCanvasHeight(self):
        """获取GL的画布高
        @rtype: int
        @return: 返回GL的画布高
        """
        return self.h

    def GetMemData(self):
        """获取数据
        @rtype: str
        @return: 返回二进制数据
        """
        GL,X11 = self.GL,self.X11
        length = self.w*self.h*4
        imgdata = (c_ubyte*length)(0)
        GL.glReadPixels(0,0,self.w,self.h,GL_RGBA,GL_UNSIGNED_BYTE,imgdata);
        data = [i for i in imgdata]
        return data

    def Output(self, path, type):
        """输出成图片
        @type path: str
        @param path: 输出图片的位置
        @type type: str
        @param path: 输出图片的类型，比如png，jpg等等
        """
        data = self.GetMemData()
        arr = Numeric.array(data,Numeric.Int8)
        arr.shape = (-1,4)
        arr = arr[:,0:3]
        ofile = path
        img = Image.fromstring("RGB",(self.w,self.h),arr.tostring()) \
                        .transpose(Image.FLIP_TOP_BOTTOM) \
                        .save(ofile,type)
