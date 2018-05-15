#-*- encoding:utf-8 -*-
"""测试操作handler
"""

import time
from geosings.workstation import ws
from geosings.core.Layer import *
from geosings.core.Symbol import *
from geosings.ui.gmap.GOperHandler import *
#from geosings.ui.UISettings import *
ws.start()
time.sleep(1)

canvas = ws.canvas
canvas.RegHandler(CharHandler(canvas))

layer = OpenV("/gisdata/guangdong/guangdong/441400.shp")
map = ws.map
map.AddLayer(layer)
ws.ReDraw()

