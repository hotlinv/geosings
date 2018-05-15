from geosings.ui.g3d.My3DCanvas import My3DRender,RunGLWin
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import Image,os
import Numeric as Num
from geosings.ui.core.MainImage import GetImageDirPath

class GlowRingRender(My3DRender):
    def __init__(self):
        My3DRender.__init__(self)
        glutInit([])
        self.teimg,self.tew,self.teh = self.ReadImage()
        self.textures = None
        self.lastx = self.x = 0
        self.lasty = self.y = 90
        self.zoom,self.zy = 0.0, 0
        self.geox,self.geoy = -118,30

    def ReadImage(self):
        imgdir = GetImageDirPath()
        imgpath = os.path.join(imgdir,'bk.png')
        img = Image.open(imgpath)
        width,height = img.size
        region =img.crop((0,0,width,height)) 
        data = region.tostring()
        return data,width,height

    def texture(self):
        textures = self.textures = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, textures)   # 2d texture (x and y size)
        
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.tew, self.teh, 0, GL_RGBA, 
                GL_UNSIGNED_BYTE, self.teimg)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


    def OnDraw(self):
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE); 
        glEnable(GL_TEXTURE_2D);
        glEnable(GL_ALPHA_TEST); 

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glColor4f(1.0,1.0,1.0,1.0)

        glBegin(GL_TRIANGLE_STRIP);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1, -1, 3);
        glTexCoord2f(0.0, 1.0);
        glVertex3f(-1, 1, 3);
        glTexCoord2f(1.0, 1.0);
        glVertex3f(1, 1, 3);
        glTexCoord2f(1.0, 0.0);
        glVertex3f(1, -1, 3);
        glTexCoord2f(0.0, 0.0);
        glVertex3f(-1, -1, 3);
        glEnd(); 

        self.SwapBuffers()

        glFlush()
        glDisable(GL_BLEND );
        glDisable(GL_ALPHA_TEST); 
        #glEnable(GL_DEPTH_TEST);
        glDisable(GL_TEXTURE_2D); 

    def InitGL(self):
        self.texture()
        glMatrixMode(GL_PROJECTION)
        gluPerspective(30.0, self.CanvWidth*1.0/self.CanvHeight, 1.0, 10.0)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST);
        glClearColor(0.0,0.0,0.0,1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glLoadIdentity()

        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
        glBindTexture(GL_TEXTURE_2D, self.textures)

if __name__=="__main__":
    RunGLWin(GlowRingRender())
