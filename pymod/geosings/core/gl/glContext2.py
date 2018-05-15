# -*- coding: utf-8 -*-
"""
该模块是进行OpenGL的离屏渲染环境的构建
该模块是用ctype建立的。
"""

import os

glOffScreenRC = 1

if os.name == 'nt':
    # windows系统
    from wglContext import wglOffScreenRC
    glOffScreenRC = wglOffScreenRC
else:
    #posix系统,X桌面环境
    from glXContext import glXOffScreenRC
    glOffScreenRC = glXOffScreenRC


if __name__ == "__main__":
    from OpenGL.GL import *
    from time import time
    context = glOffScreenRC(300,300)


    glShadeModel( GL_FLAT );
    glClearColor( 0.0, 0.5, 0.0, 1.0 );
    glClear( GL_COLOR_BUFFER_BIT );
    glViewport( 0, 0, 300, 300 );
    glOrtho( -1.0, 1.0, -1.0, 1.0, -1.0, 1.0 );
    glColor3f( 0.0, 1.0, 1.0 );
    glRectf( -0.75, -0.75, 0.75, 0.75 );
    glFlush();

    beg = time()

    context.Output('./output.png','png')

    print time()-beg
