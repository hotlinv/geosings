#-*- encoding:utf-8 -*-
"""测试地图导出
"""

import time,Image
from geosings.workstation import ws,screen2img
from geosings.core.Layer import *
from geosings.core.Symbol import *
from geosings.ui.gmap.LayerRender import *
from geosings.core.Annotate import AnnotateProps

ws.start()
time.sleep(1)

names = ["440100","440200",'440300',
		'440400','440500',"440600",
		'440700','440800','440900',
		'441200',"441300","441400",
		"441500","441600","441700",
		"441800","441900","442000",
		"445100","445200","445300",
		"guangdong2Copy"
		]

class OutputPointRender(VectorRender):
    def __init__(self, layer, conf):
        """构造函数，conf需要有points字段
        """
        VectorRender.__init__(self, layer)
        self.conf = conf
        self.conf['points'] = {}
        self.featureDrawMap[ogr.wkbPoint] = self._DrawPoint

    def Draw(self,dc,wprect,wgrect):
        try:
            x,y,w,h,bw,bh,mx,my = self.layer.CacDrawArgs(wprect,wgrect)
            scale = bh*1.0/h
        except Exception, args:
            error('CacDrawArgs false1 : %s',args)
            return
        self.dcrect = wprect
        self.minx = self.layer.DataGeoExt.GetLeft()
        self.maxy = self.layer.DataGeoExt.GetTop()

        dataset = self.layer.DataSet()
        feature = dataset.GetNextFeature()
        while feature:
            geomref = feature.GetGeometryRef()
            geomreftype = geomref.GetGeometryType()
            drawFun = self.featureDrawMap[geomreftype]
            drawFun(dc,feature.GetField('ADCODE93'),geomref,scale,x,y,mx,my)
            feature = dataset.GetNextFeature()
    def _DrawPoint(self,dc,fid,georef,scale,x,y,mx,my):
        """绘制点
        @type georef: GDAL Geometry
        @param georef: 要绘制的几何形状
        @type scale: float
        @param scale: XY需要缩放的倍数
        @type x,y: number
        @param x,y: 返回图像的X,Y
        @type mx,my: number
        @param mx,my: 在地图矩形中的图像的X,Y
        """
        points = self._GetPoints(georef,scale,x,y,mx,my)
        #dc.DrawCirclePoint(points[0],self.symsize)
        point = points.astype(Int)[0]
        self.conf['points'][fid]=[point[0],point[1]]

ws.resize((800,500))

def extrect(geoext):
    exw = geoext.GetWidth()*0.1
    exh = geoext.GetHeight()*0.1
    print exw,exh
    return GeoRect(geoext.GetLeft()-exw, geoext.GetTop()+exh, 
            geoext.GetRight()+exw, geoext.GetBottom()-exh)
    

map = ws.map
ws.canvas.LABEL_ALONE=True#立即标注，不要统一标注
#背景图层
layersea = OpenV("/gisdata/guangdong/sea/sea.shp")
layersea.symbol['color'] = "#aaf8fe"
#layersea.labelProps = AnnotateProps({"field":"name"})
map.AddLayer(layersea)

PROV_COLOR = "#efefef99"
#省份标注字体
FONT_STY = {"field":"name99","font":u"华文行楷","size":18,"color":"#ff0000","bold":True}

layerprov = OpenV("/gisdata/guangdong/bount_poly_prov.shp")
layerprov.symbol['color'] = PROV_COLOR
layerprov.labelProps = AnnotateProps(FONT_STY)
map.AddLayer(layerprov)

layerlineb = OpenV("/gisdata/guangdong/bount_line_prov.shp")
layerlineb.symbol["color"] = "#aeaedbaa"
layerlineb.symbol["size"] = 12
map.AddLayer(layerlineb)

layerline = OpenV("/gisdata/guangdong/bount_line_prov.shp")
layerline.symbol["color"] = "#ff0000"
layerline.symbol["size"] = 2
layerline.symbol["hatch"] = wx.DOT_DASH
#layerline.symbol['color'] = PROV_COLOR
#layerline.labelProps = AnnotateProps(FONT_STY)
map.AddLayer(layerline)

layerb = OpenV("/gisdata/guangdong/guangdong/guangdong2Copy.shp")
layerb.symbol['color'] = PROV_COLOR
layerb.labelProps = AnnotateProps({"color":"#000000", "size":8})
map.AddLayer(layerb)

for name in names:
    context = {'points':{}}
    
    layerp = OpenV("/gisdata/guangdong/city/"+name+".shp")
    #通过render,控制context导出县市位置
    layerp.render = OutputPointRender(layerp,context) 
    map.AddLayer(layerp)

    layer = OpenV("/gisdata/guangdong/guangdong/"+name+".shp")
    layer.symbol = CreateUniqueSymbol('code')
    map.AddLayer(layer)
    #print layer.geoext
    ws.canvas.geoext = extrect(layer.geoext)
    #print ws.canvas.geoext
    ws.ReDraw()
    
    #time.sleep(1)

    #导出tif图片
    screen2img(ws.canvas, "/gisdata/guangdong/guangdong/"+name+".tif")
    
    #导出颜色列表
    f = open("/gisdata/guangdong/guangdongpng/"+name+".txt",'w')
    for k in layer.symbol['colormap']:
        layer.symbol['colormap'][k] = layer.symbol['colormap'][k][:-2]
    f.write( str(layer.symbol['colormap']) )
    f.close()

    #重新设置图层的显示范围
    map.RemoveLayer(layerp)
    map.RemoveLayer(layer)
    ws.canvas.geoext = None
    #ws.ReDraw()

    #导出png图片
    im = Image.open("/gisdata/guangdong/guangdong/"+name+".tif")
    im.save("/gisdata/guangdong/guangdongpng/"+name+".png", 'png')
    del im

    #导出配置
    file = open("/gisdata/guangdong/guangdongpng/"+name+".txt")
    d = file.read()
    a = eval( d )
    #导出颜色列表
    #print context['points']
    #print a
    for key in [int(i) for i in a.keys() if i is not None]:
        if key not in context['points'] and key+1 not in context['points']:
            context['points'][key] = [0,0]
        elif key+1 in context['points'] and key % 100==0:
            context['points'][key+1].append(a[key])
        else:
            context['points'][key].append(a[key])
    #print context['points']
    of = open("/gisdata/guangdong/guangdongpng/"+name+".json",'w')
    of.write(str(context))
    of.close()
    file.close()

    print u"导出成功"

import sys
sys.exit(0)
