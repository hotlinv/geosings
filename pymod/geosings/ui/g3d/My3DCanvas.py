# -*- coding: utf-8 -*-
#writer:linux_23; create:2007.7.6 ; version:1; 创建
"""
这里是定义3d显示画板的模块
"""

from wxPython.glcanvas import wxGLCanvas
from wxPython.wx import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys,math,wx
import geosings.core.system.UseGetText

class MyGLCanvas(wxGLCanvas):
    def __init__(self, parent, render):
        wxGLCanvas.__init__(self, parent,-1)
        self.init = 0
        self.render = render
        self.render._SetCanv(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

    def OnPaint(self,event):
        dc = wxPaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.render.InitGL()
            self.init = 1
        self.render.OnDraw()

    def OnSize(self,event):
        self.render.ReSize()

    def OnLeftDown(self,evt):
        self.render.OnLeftDown(evt)
    def OnLeftUp(self,evt):
        self.render.OnLeftUp(evt)
    def OnRightDown(self,evt):
        self.render.OnRightDown(evt)
    def OnRightUp(self,evt):
        self.render.OnRightUp(evt)
    def OnMouseMove(self,evt):
        self.render.OnMouseMove(evt)


class My3DRender:
    """所有3D渲染类的基类
    """
    def __init__(self):
        self.canv = None
    def _SetCanv(self, parentCanv):
        self.canv = parentCanv
        self.SwapBuffers = self.canv.SwapBuffers
        self.CanvWidth,self.CanvHeight = self.canv.GetClientSizeTuple()

    def ReSize(self):
        if self.canv:
            self.CanvWidth,self.CanvHeight = self.canv.GetClientSizeTuple()
            glViewport(0, 0, self.CanvWidth, self.CanvHeight)
            #self.OnDraw()

    def OnDraw(self):
        """绘制函数，等着被继承
        """
        pass
    def InitGL(self):
        """初始化GL，等着被继承
        """
        pass
    def OnLeftDown(self,evt):
        pass
    def OnLeftUp(self,evt):
        pass
    def OnRightDown(self,evt):
        pass
    def OnRightUp(self,evt):
        pass
    def OnMouseMove(self,evt):
        pass

class TestRender(My3DRender):
    """测试渲染类
    """
    def __init__(self):
        My3DRender.__init__(self)

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        # draw six faces of a cube
        glBegin(GL_QUADS)
        glNormal3f( 0.0, 0.0, 1.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5,-0.5, 0.5)
        glVertex3f( 0.5,-0.5, 0.5)

        glNormal3f( 0.0, 0.0,-1.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glVertex3f( 0.5, 0.5,-0.5)
        glVertex3f( 0.5,-0.5,-0.5)

        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f( 0.5, 0.5,-0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glNormal3f( 0.0,-1.0, 0.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f( 0.5,-0.5,-0.5)
        glVertex3f( 0.5,-0.5, 0.5)
        glVertex3f(-0.5,-0.5, 0.5)

        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f( 0.5,-0.5, 0.5)
        glVertex3f( 0.5,-0.5,-0.5)
        glVertex3f( 0.5, 0.5,-0.5)

        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5,-0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glEnd()

        #glRotatef((self.lasty - self.y)/100., 1.0, 0.0, 0.0);
        #glRotatef((self.lastx - self.x)/100., 0.0, 1.0, 0.0);

        self.SwapBuffers()


    def InitGL(self):
        glMatrixMode(GL_PROJECTION);
        glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0);

        # position viewer
        glMatrixMode(GL_MODELVIEW);
        glTranslatef(0.0, 0.0, -2.0);

        # position object
        glRotatef(3.2, 1.0, 0.0, 0.0);
        #glRotatef(self.x, 0.0, 1.0, 0.0);

        glEnable(GL_DEPTH_TEST);
        glEnable(GL_LIGHTING);
        glEnable(GL_LIGHT0);


class My3dFrame(wx.Frame):
    def __init__(self, parent, render):
        wx.Frame.__init__(self,parent,-1,"UniverseRing", wxDefaultPosition,
                wx.Size(500,500))
        canvas = MyGLCanvas(self, render)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(canvas, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()

def RunGLWin(render):
    app = wxPySimpleApp()
    frame = My3dFrame(None,render)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__': RunGLWin(TestRender())
