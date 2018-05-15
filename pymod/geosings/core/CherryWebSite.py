# -*- coding:utf-8 -*-
"""
这里是建立小型数据服务器的地方

 - writer:linux_23; create:2008.5.29 ; version:1; 创建
"""

import sys
#if sys.getdefaultencoding() != 'utf-8':
#    reload(sys)
#    sys.setdefaultencoding('utf-8')


import os,webbrowser,threading
from geosings.core.system.DefConf import GSSHOME
cherrypath = os.path.join(GSSHOME,"CherryPy-3.0.3.zip")
sys.path.append( cherrypath )

import cherrypy
from geosings.core.gssconst import DataSetType
from geosings.tools.ReportLayerInfo import ReportLayerInfoCtrl
from geosings.core.Layer import *
from geosings.core.system.EncodeTran import *

class WebSite:
    #_cpFilterList = [EncodingFilter('utf8')]
    @cherrypy.expose
    def LayerInfos(self,layer,t=DataSetType.Vector):
        if type(t)==str:
            t = int(t)
        if t==DataSetType.Vector:
            vlayer = OpenV(layer)
        else:
            vlayer = OpenR(layer)
        infoctrl = ReportLayerInfoCtrl(vlayer)
        info = utf82locale(infoctrl.Report())
        return info

def call_cherryws():
    wsapp = WebSite()
    cherrypy.server.socket_port = 2386
    conf = {"/css":{"tools.staticdir.on":True,
                    "tools.staticdir.dir": os.path.join(GSSHOME,'resource','css')},
            "/js":{"tools.staticdir.on":True,
                    "tools.staticdir.dir": os.path.join(GSSHOME,
                        "resource", "js")},
            "/images":{"tools.staticdir.on":True,
                    "tools.staticdir.dir": os.path.join(GSSHOME,
                        "resource", "images")}
            }
    cherrypy.quickstart(wsapp,'/', config=conf)

class WebSiteThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        call_cherry()

def start_website():
    #ws = WebSiteThread()
    wst = threading.Thread(target=call_cherryws,args = [])
    wst.start()
def stop_website():
    cherrypy.server.stop()
#cherrypy.stop()

if __name__=="__main__":
    start_website()
    import time
    #time.sleep(5)
    stop_website()
    print 'end'
    #import sys
    #sys.exit(0)
else:
    call_cherryws()
