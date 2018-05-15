# -*- coding: utf-8 -*-

from ctypes import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.WGL import *
import Numeric, Image

BI_RGB = 0

if 'PFD_DRAW_TO_BITMAP' not in dir():
    PFD_DRAW_TO_BITMAP = 0x00000008
if 'PFD_SUPPORT_OPENGL' not in dir():
    PFD_SUPPORT_OPENGL = 0x00000020
if 'PFD_MAIN_PLANE' not in dir():
    PFD_MAIN_PLANE = 0
if 'PFD_TYPE_RGBA' not in dir():
    PFD_TYPE_RGBA = 0

class BITMAPINFOHEADER(Structure):
    """定义BITMAPINFOHEADER结构体
    """
    _fields_ = [("biSize", c_ulong),
                ("biWidth", c_long),
                ("biHeight", c_long),
                ("biPlanes", c_ushort),
                ("biBitCount", c_ushort),
                ("biCompression", c_ulong),
                ("biSizeImage", c_ulong),
                ("biXPelsPerMeter", c_long),
                ("biYPelsPerMeter", c_long),
                ("biClrUsed", c_ulong),
                ("biClrImportant", c_ulong),
            ]
class RGBQUAD(Structure):
    """定义RGBQUAD结构体
    """
    _fields_ = [('rgbBlue',c_ushort),
                ('rgbGreen',c_ushort),
                ('rgbRed',c_ushort),
                ('rgbReserved',c_ushort),
            ]
class BITMAPINFO(Structure):
    """定义BITMAPINFO结构体
    """
    _fields_ = [("BITMAPINFOHEADER",BITMAPINFOHEADER),
                ("RGBQUAD", c_ushort),#RGBQUAD bmiColors[1]; 
                ]
class PIXELFORMATDESCRIPTOR(Structure):
    """定义PIXELFORMATDESCRIPTOR结构体
    """
    _fields_ = [('nSize',c_ushort),
                ('nVersion',c_ushort),
                ('dwFlags',c_ulong),
                ('iPixelType',c_ubyte),
                ('cColorBits',c_ubyte),
                ('cRedBits',c_ubyte),
                ('cRedShift',c_ubyte),
                ('cGreenBits',c_ubyte),
                ('cGreenShift',c_ubyte),
                ('cBlueBits',c_ubyte),
                ('cBlueShift',c_ubyte),
                ('cAlphaBits',c_ubyte),
                ('cAlphaShift',c_ubyte),
                ('cAccumBits',c_ubyte),
                ('cAccumRedBits',c_ubyte),
                ('cAccumGreenBits',c_ubyte),
                ('cAccumBlueBits',c_ubyte),
                ('cAccumAlphaBits',c_ubyte),
                ('cDepthBits',c_ubyte),
                ('cStencilBits',c_ubyte),
                ('cAuxBuffers',c_ubyte),
                ('iLayerType',c_ubyte),
                ('bReserved',c_ubyte),
                ('dwLayerMask',c_ulong),
                ('dwVisibleMask',c_ulong),
                ('dwDamageMask',c_ulong),
            ]

class wglOffScreenRC:
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
        self.w ,self.h = w,h
        self.hdc = windll.gdi32.CreateCompatibleDC(0)
        if self.hdc == 0: raise "hdc build failed!"
        bmi = BITMAPINFO(
                BITMAPINFOHEADER(sizeof(BITMAPINFOHEADER),self.w,self.h,1,32,
                BI_RGB,0,0,0,0,0),
                c_ushort(0))
        self.pbits = c_voidp(0)
        self.hbm = windll.gdi32.CreateDIBSection(self.hdc, pointer(bmi), 0,
                pointer(self.pbits), 0, 0)
        if self.hbm == 0: raise "hbm build failed!"
        self.r = windll.gdi32.SelectObject(self.hdc,self.hbm)
        if self.r == 0: raise "r build failed!"
        pfd = PIXELFORMATDESCRIPTOR(sizeof (PIXELFORMATDESCRIPTOR), 
                                1,
                                PFD_DRAW_TO_BITMAP | PFD_SUPPORT_OPENGL, 
                                PFD_TYPE_RGBA, 
                                32, 
                                0, 0, 0, 
                                0, 0, 0, 
                                0, 0,
                                0, 0, 0, 0, 0, 
                                32, 0, 0, 
                                PFD_MAIN_PLANE, 
                                0, 0, 0, 0 )
        pfid = windll.gdi32.ChoosePixelFormat(self.hdc,pointer(pfd))
        if pfid == 0: raise 'pfid build failed'
        b = windll.gdi32.SetPixelFormat(self.hdc,pfid,pointer(pfd))
        if not b: raise 'setpixelformat failed'
        self.hglrc = windll.opengl32.wglCreateContext(self.hdc)
        if self.hglrc == 0: raise "hglrc build failed"
        windll.opengl32.wglMakeCurrent(self.hdc, self.hglrc)
        
        self.enable = True

    def Destroy(self):
        """销毁GL的画布
        """
        if windll is not None:
            windll.opengl32.wglDeleteContext(self.hglrc)
            windll.gdi32.SelectObject(self.hdc, self.r)
            windll.gdi32.DeleteObject(self.hbm)
            windll.gdi32.DeleteDC(self.hdc)
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
        length = self.w*self.h*4
        imgdata = (c_ubyte*length)(0)
        #print '&'*30,windll
        #windll.opengl32.glReadPixels(0,0,self.w,self.h,GL_RGBA,GL_UNSIGNED_BYTE,imgdata);
        imgdata = cast(self.pbits, POINTER(c_ubyte))
        data = [imgdata[i] for i in range(length)]
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

if __name__ == '__main__':
    #测试代码
    context = wglOffScreenRC(300,300)

    glClearColor(0.9,0.9,0.3,1.0);
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    gluPerspective(30.0, 1.0, 1.0, 10.0);
    glMatrixMode(GL_MODELVIEW);
    gluLookAt(0, 0, -5, 0, 0, 0, 0, 1, 0);
    glBegin(GL_TRIANGLES);
    glColor3d(1, 0, 0);
    glVertex3d(0, 1, 0);
    glColor3d(0, 1, 0);
    glVertex3d(-1, -1, 0);
    glColor3d(0, 0, 1);
    glVertex3d(1, -1, 0);
    glEnd();
    glFlush();
    

    context.Output('./tt1.png','png')
    context.Destroy()
