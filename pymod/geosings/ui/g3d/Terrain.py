# -*- coding: utf-8 -*-
#writer:linux_23; create:2007.7.7 ; version:1; 创建
"""
地形可视化程序
"""
from geosings.ui.g3d.My3DCanvas import My3DRender,RunGLWin
from geosings.core.Layer import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Numeric as Num
import Image,gdal

class TerrainRender(My3DRender):
    def __init__(self,raslayer):
        My3DRender.__init__(self)
        glutInit([])#linux下需要加这句
        self.teimg,self.tew,self.teh = self.ReadImage(raslayer)
        #self.textures = None
        self.lastx = self.x = 0
        self.lasty = self.y = 0
        self.zoom,self.zy = 0.0, 0
        self.geox,self.geoy = -0,0

    def ReadImage(self,raslayer):
        dataset = raslayer.DataSet()
        width,height = dataset.RasterXSize,dataset.RasterYSize
        band = dataset.GetRasterBand(1)
        data = dataset.ReadAsArray(0,0,width,height)
        #data = img.tostring("raw", "RGBX", 0, -1)
        points = data[::4,::4]
        #print points
        width = points.shape[1]
        height = points.shape[0]
        return points,width,height

    def DrawTerrain(self):
        points = data = self.teimg
        width = self.tew
        height = self.teh
        
        glBegin(GL_QUADS)
        hw = width/2
        hh = height/2
        for y in range(height-1):
            for x in range(width-1):
                #glTexCoord2f( float_x, float_y);
                c = points[y,x]/255.0
                glColor3f(c, c, c )
                glVertex3f( (x-hw)/20.0, (y-hh)/20.0, points[y,x]/10.0/255 )

                #glTexCoord2f( float_x, float_yb );
                glVertex3f( (x-hw+1)/20.0, (y-hh)/20.0, points[y,x+1]/10.0/255 )

                #glTexCoord2f( float_xb, float_yb );
                #glColor3f( data[y+1,x+1], data[y+1,x+1], data[y+1,x+1] )
                glVertex3f( (x-hw+1)/20.0, (y-hh+1)/20.0,
                        points[y+1,x+1]/10.0/255 )

                #glTexCoord2f( float_xb, float_y );
                #glColor3f( data[y+1,x], data[y+1,x], data[y+1,x] )
                glVertex3f( (x-hw)/20.0, (y-hh+1)/20.0, points[y+1,x]/10.0/255 )
        glEnd()

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glPushMatrix()################################
        self.geoy += -(self.lasty - self.y)/50.
        self.geox += -(self.lastx - self.x)/50.
        #print self.zoom
        glTranslate(0.0,0.0,self.zoom)
        #print self.geox, self.geoy
        glRotatef(self.geoy, 1.0, 0.0, 0.0);
        glRotatef(self.geox, 0.0, 1.0, 0.0);
        glPushMatrix()####################
        glRotatef(-90.0,1.0,0.0,0.0)			# Rotate The Cube On It's X Axis
        #glRotatef(0.0,0.0,1.0,0.0)			# Rotate The Cube On It's Y Axis
        #glRotatef(-100.0,0.0,0.0,1.0)			# Rotate The Cube On It's Z Axis
        self.DrawTerrain()
        glPopMatrix()#####################
        glPopMatrix()##################################
        self.SwapBuffers()
        glFlush()

    def InitGL(self):
        #self.texture()
        glMatrixMode(GL_PROJECTION)
        gluPerspective(30.0, self.CanvWidth*1.0/self.CanvHeight, 1.0, 10.0)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST);
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glShadeModel(GL_FLAT)

        
        glLoadIdentity()

        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
        #glBindTexture(GL_TEXTURE_2D, self.textures[0])

    def OnLeftDown(self,evt):
        self.canv.CaptureMouse()
        self.lastx, self.lasty = evt.GetPosition()
    def OnLeftUp(self,evt):
        self.canv.ReleaseMouse()
        self.x ,self.y = self.lastx,self.lasty
    def OnRightDown(self,evt):
        self.canv.CaptureMouse()
        x, self.zy = evt.GetPosition()
    def OnRightUp(self,evt):
        self.canv.ReleaseMouse()
    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.x, self.y = evt.GetPosition()
            self.canv.Refresh(False)
        elif evt.Dragging() and evt.RightIsDown():
            mx, my = evt.GetPosition()
            if self.zy-my>0:
                self.zoom += 0.2
            else:
                self.zoom -= 0.2
            self.canv.Refresh(False)

if __name__=="__main__":
    ras = Layer.Open("J:/gisdata/gtif/dem.tif")
    RunGLWin(TerrainRender(ras))
