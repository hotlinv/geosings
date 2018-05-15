# -*- encoding: utf-8 -*-
import os
import sys,glob

#prefix = sys.prefix
#scriptdir = os.path.join(prefix,'Scripts')
#easy_inst = os.path.join(scriptdir, 'easy_install.exe')
#if not os.access(easy_inst,os.F_OK):
#    print u'请安装easy_install工具'
#    sys.exit(1)
easy_inst = 'ez_setup.py'

pkgs = [
        ['Numeric','Numeric','Numeric'],
        ['PIL','PIL','Image'],
        ['wxPython','wxPython','wx'],
        ['django','django','django'],
        ['ctypes','ctypes','ctypes'],
        ['PyOpenGL','PyOpenGL','OpenGL.GL'],
        ['pysqlite2','pysqlite','pysqlite2'],
        ]


def instpkg(name,instname,importname):
    try:
        print u'检查'+name+u'是否安装...',
        exec('import '+importname)
        print u'\r已安装'+name+u',忽略...'
    except:
        print u'\r未安装。正在安装'+name+'...'
        if name == 'wxPython':
            wxpy = glob.glob('wxPython*.exe')
            if len(wxpy):
                os.system(wxpy[len(wxpy)-1])
            else:
                print u"安装wxPython没有成功，您可能需要手动安装"
        elif name == 'django':
            pwd = os.getcwd()
            djangopath = glob.glob('Django*')
            for i in djangopath:
                if os.path.isdir(i):
                    os.chdir(i)
                    os.system("setup.py install")
                    os.chdir(pwd)
                    break
        else:
            os.system(easy_inst+' -f ./ '+instname)


for pkg in pkgs:
    instpkg(pkg[0],pkg[1],pkg[2])


