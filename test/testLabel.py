#-*- encoding:utf-8 -*-
"""测试地图标注
"""

import time

from geosings.workstation import ws, screen2img
from geosings.core.Layer import *
from geosings.core.Annotate import AnnotateProps
from geosings.core.system.EncodeTran import *


ws.start()
time.sleep(1)

ws.resize((800,600))

#layer = OpenV("/gisdata/guangdong/city/city.shp")

#隶书前面的u相当重要！
FONT_STY = {"font":u"隶书","size":8,"color":"#ff0000","bold":True}
layer2 = OpenV("/gisdata/guangdong/guangdong/guangdong2Copy.shp")
layer2.labelProps = AnnotateProps(FONT_STY)

map = ws.map
map.AddLayer(layer2)
#map.AddLayer(layer)
ws.ReDraw()

