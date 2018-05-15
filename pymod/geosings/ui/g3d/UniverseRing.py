# -*- coding: utf-8 -*-
#writer:linux_23; create:2007.7.6 ; version:1; 创建
"""
类似GoogleEarth的程序
"""

from geosings.ui.g3d.My3DCanvas import My3DRender,RunGLWin
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Image,os
import Numeric as Num
from geosings.ui.core.MainImage import GetImageDirPath

class UniverseRingRender(My3DRender):
    def __init__(self):
        My3DRender.__init__(self)
        glutInit([])#linux下需要加这句
        self.teimg,self.tew,self.teh = self.ReadImage()
        self.bkimg,self.bkw,self.bkh = self.ReadGlowImage()
        self.textures = None
        self.lastx = self.x = 0
        self.lasty = self.y = 90
        self.zoom,self.zy = 0.0, 0
        self.geox,self.geoy = -118,30
    def ReadGlowImage(self):
        imgdir = GetImageDirPath()
        imgpath = os.path.join(imgdir,'bk.png')
        img = Image.open(imgpath)
        width,height = img.size
        region =img.crop((0,0,width,height)) 
        data = region.tostring()
        return data,width,height

    def ReadImage(self):
        imgdir = GetImageDirPath()
        imgpath = os.path.join(imgdir,'world.jpg')
        img = Image.open(imgpath)
        width,height = img.size
        data = img.tostring("raw", "RGBX", 0, -1)
        return data,width,height

    def texture(self):
        textures = self.textures = glGenTextures(4)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glBindTexture(GL_TEXTURE_2D, textures[0])   # 2d texture (x and y size)

        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.tew, self.teh, 0, GL_RGBA,
            GL_UNSIGNED_BYTE, self.teimg)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        # Create Linear Filtered Texture 
        glBindTexture(GL_TEXTURE_2D, textures[1])
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.tew, self.teh, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, self.teimg)

        # Create MipMapped Texture
        glBindTexture(GL_TEXTURE_2D, textures[2])
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3, self.tew, self.teh, GL_RGBA,
                GL_UNSIGNED_BYTE, self.teimg)

        quadratic = self.quadratic = gluNewQuadric()
        
        gluQuadricNormals(quadratic, GLU_SMOOTH)		# Create Smooth Normals (NEW) 
        gluQuadricTexture(quadratic, GL_TRUE)			# Create Texture Coords (NEW) 

        # Create Bk glow Texture
        glBindTexture(GL_TEXTURE_2D, textures[3])   # 2d texture (x and y size)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.bkw, self.bkh, 0, GL_RGBA, 
                GL_UNSIGNED_BYTE, self.bkimg)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        glEnable(GL_TEXTURE_2D)

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glPushMatrix()################################
        self.geoy += -(self.lasty - self.y)/50.
        self.geox += -(self.lastx - self.x)/50.
        print self.zoom
        glTranslate(0.0,0.0,self.zoom)
        print self.geox, self.geoy
        glRotatef(self.geoy, 1.0, 0.0, 0.0);
        glRotatef(self.geox, 0.0, 1.0, 0.0);
        glPushMatrix()####################
        glRotatef(-90.0,1.0,0.0,0.0)			# Rotate The Cube On It's X Axis
        #glRotatef(0.0,0.0,1.0,0.0)			# Rotate The Cube On It's Y Axis
        #glRotatef(-100.0,0.0,0.0,1.0)			# Rotate The Cube On It's Z Axis
        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        gluSphere(self.quadratic,2.3,512,256)
        glPopMatrix()#####################
        glPopMatrix()##################################
        self.DrawGlow()
        self.SwapBuffers()
        glFlush()
    def DrawGlow(self):
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE); 
        glEnable(GL_TEXTURE_2D);
        glEnable(GL_ALPHA_TEST); 
        glBindTexture(GL_TEXTURE_2D, self.textures[3])

        glColor4f(1.0,1.0,1.0,1.0)

        glBegin(GL_TRIANGLE_STRIP);
        r = 6.2
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1, -1, r);
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-1, 1, r);
        glTexCoord2f(1.0, 1.0);
        glVertex3f(1, 1, r);
        glTexCoord2f(1.0, 0.0);
        glVertex3f(1, -1, r);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1, -1, r);
        glEnd(); 
        glDisable(GL_BLEND );
        glDisable(GL_ALPHA_TEST); 


    def InitGL(self):
        self.texture()
        glMatrixMode(GL_PROJECTION)
        gluPerspective(30.0, self.CanvWidth*1.0/self.CanvHeight, 1.0, 10.0)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST);
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()

        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

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
                self.zoom += 0.1
            else:
                self.zoom -= 0.1
            self.canv.Refresh(False)

if __name__=="__main__":
    RunGLWin(UniverseRingRender())
