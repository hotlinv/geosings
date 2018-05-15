# -*- coding:UTF-8 -*-
#!/usr/bin/env python

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import sys,os,webbrowser
from geosings.core.system.DefConf import GSSHOME
cherrypath = os.path.join(GSSHOME,"CherryPy-3.0.3.zip")
sys.path.append( cherrypath )

import cherrypy

class HelloWorld:
    #_cpFilterList = [EncodingFilter('utf8')]
    @cherrypy.expose
    def hello(self,layer):
        return "<input type='button' onclick='alert(1);' value='我%s'/>" % layer

print webbrowser.open_new("http://localhost:8080/hello?layer=asss")

cherrypy.quickstart(HelloWorld())


