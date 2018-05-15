#-*- encoding:utf-8 -*-
"""测试唯一值
"""

import time
from geosings.workstation import ws
from geosings.core.Layer import *
from geosings.core.Symbol import *
ws.start()
time.sleep(1)

layer = OpenV("/gisdata/guangdong/guangdong/441400.shp")
layer.symbol = CreateUniqueSymbol('code')
map = ws.map
map.AddLayer(layer)
ws.ReDraw()

