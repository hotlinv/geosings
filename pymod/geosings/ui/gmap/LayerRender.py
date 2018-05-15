# -*- coding: utf-8 -*-
"""
定义图层的画板控件

 - writer:linux_23; create: 2008.4.13; version:1; 创建
"""
import wx,os,ogr,time,math
from Numeric import *
from geosings.core.gssconst import *
from geosings.core.Exception import *
from geosings.core.GeoRect import GetGeoRectGeometry
from geosings.ui.core.wxSymbol import *
from geosings.ui.core.wxFont import *
from geosings.core.LabelLayout import LabelLayout,GetBetterCentroid
from geosings.core.Geom import *
from geosings.core.GeoRect import GetGeoRectGeometry
from geosings.core.system.EncodeTran import *
from geosings.core.system.GLog import *
from geosings.core.GeoRect import *


def GDC(dc):
    try:
        return wx.GCDC(dc)
    except NotImplementedError:
        return dc

class LayerRender:
    """图层画板控件的基类
    """
    def Create(layer):
        """创建控件（静态方法）
        @type layer: L{geosings.core.Layer}
        @param layer: 要创建画板的图层
        """
        if layer.type == DataSetType.Vector:
            return VectorRender(layer)
        elif layer.type == DataSetType.Raster:
            return RasterRender(layer)
        else:
            return None
    Create = staticmethod(Create)

    def Draw(self,dc,wprect,wgrect):
        """绘制图层，往后的子类都要继承这个方法
        @type dc: wxDC
        @param dc: 绘制可用的DC
        @type wprect: L{geosings.core.GeoRect}
        @param wprect: DC的范围，主要用于分辨率判断
        @type wgrect: L{geosings.core.GeoRect}
        @param wgrect: 地图的地理范围
        """
        pass


class LabelRender(LayerRender):
    """标注绘制类
    """
    def __init__(self):
        self.points = []
        self.lines = []
        self.polygons = []
        self.label = False

    def AddPointsLab(self, symbol, points):
        """添加点标注群
        """
        if points == []: return
        self.label = True
        self.points.append([symbol,points])

    def AddLinesLab(self, symbol, lines):
        """添加线标注群
        """
        if lines == []: return
        self.label = True
        self.lines.append([symbol, lines])

    def AddPolygonsLab(self, symbol, polygons):
        """添加多边形标注群
        """
        if polygons == []: return
        self.label = True
        self.polygons.append([symbol, polygons])

    def Draw(self,dc,dcrect, wgrect):
        """标志绘制方法
        """
        #开始绘制Label
        if self.label: 
            dcr=wx.Rect(0,0,int(dcrect.GetWidth()),int(dcrect.GetHeight()))
            sl = LabelLayout({"dc":dc,
                "fontclass":FontUtils,
                "polygons":self.polygons,
                "points":self.points,
                "lines":self.lines,
                "off":5,
                },dcr)
            syms = sl.Layout()
            for sym in syms:
                symbol = sym[2]
                font = getFontSymbol(symbol)
                dc.SetFont(font)
                bc = getFontBColorSymbol(symbol)
                if bc:
                    dc.SetBackgroundMode(wx.SOLID)
                    dc.SetTextBackground(bc)# set back color
                else:
                    dc.SetBackgroundMode(wx.TRANSPARENT)
                fc = getFontFColorSymbol(symbol)
                if fc: dc.SetTextForeground(fc)# set fore color
                #fsize = sl.GetFontSize(sym[1])
                #dc.DrawRectangle(sym[0][0],sym[0][1],fsize[0],fsize[1])
                dc.DrawText(sym[1], sym[0][0], sym[0][1])


class VectorRender(LayerRender):
    """矢量图层的画板
    """
    def __init__(self,layer):
        """初始化画板
        @type layer: L{geosings.core.Layer}
        @param layer: 初始化画板的图层
        """
        self.layer = layer
        FeatureDrawMap = {
            ogr.wkbPoint:self.__DrawPoint,
            ogr.wkbMultiPoint:self.__DrawPoints,
            ogr.wkbLineString:self.__DrawLine,
            ogr.wkbMultiLineString:self.__DrawLines,
            ogr.wkbPolygon:self.__DrawPolygon,
            ogr.wkbMultiPolygon:self.__DrawPolygons
        }
        self.featureDrawMap = FeatureDrawMap
        self.labelCanvas = None
        self.label = None

    def Draw(self,dc,wprect,wgrect):
        """绘制图层
        @type dc: wxDC
        @param dc: 绘制可用的DC
        @type wprect: L{geosings.core.GeoRect}
        @param wprect: DC的范围，主要用于分辨率判断
        @type wgrect: L{geosings.core.GeoRect}
        @param wgrect: 地图的地理范围
        """
        try:
            x,y,w,h,bw,bh,mx,my = self.layer.CacDrawArgs(wprect,wgrect)
            scale = bh*1.0/h
        except Exception, args:
            error('CacDrawArgs false: %s',str(args))
            return
        gc = GDC(dc)#换到GC,支持透明
        self.dcrect = wprect
        star = time.time()
        self.ctime = 0
        self.symbol = self.layer.symbol
        debug(self.symbol)
        self.label = label = self.layer.labelProps#要不要画Label
        if label :
            self.labelps = labelps = []
            self.labells = labells = []
            self.labelpls = labelpls = []
        dataset = self.layer.DataSet()
        exgeom = GetGeoRectGeometry(wgrect)
        dataset.SetSpatialFilter(exgeom)
        featurecount = dataset.GetFeatureCount()
        dataset.ResetReading()
        layerGeomT = dataset.GetLayerDefn().GetGeomType()
        #if layerGeomT==ogr.wkbUnknown:
        pen = getPanSymbol(self.symbol)#wx.BLACK_PEN
        brush = getBrushSymbol(self.symbol)#wx.RED_BRUSH
        self.symsize = getSizeSymbol(self.symbol)
        gc.SetPen(pen)
        gc.SetBrush(brush)
        self.minx = self.layer.DataGeoExt.GetLeft()
        self.maxy = self.layer.DataGeoExt.GetTop()
            
        #开始循环绘制Feature
        feature = dataset.GetNextFeature()
        while feature:
            if label:
                try:
                    self.labstrnow = feature.GetField(label.field)
                    if not self.labstrnow: self.labstrnow = u""
                    else: self.labstrnow = astr2utf8(self.labstrnow)
                except Exception,e:
                    self.label = label = self.layer.labelProps = None
                    raise FieldNotFoundErr(e)
            if self.symbol['type']==SymbolType.UNIQUE:
                fname = self.symbol['field']
                brush = getBrushSymbol(self.symbol, feature.GetField(fname))
                gc.SetBrush(brush)
            geomref = feature.GetGeometryRef()
            geomreftype = geomref.GetGeometryType()
            drawFun = self.featureDrawMap[geomreftype]
            drawFun(gc,geomref,pen,brush,scale,x,y,mx,my)
            feature = dataset.GetNextFeature()

        if label:
            self.labelCanvas.AddPointsLab(self.label.symbol,labelps)
            self.labelCanvas.AddLinesLab(self.label.symbol,labells)
            self.labelCanvas.AddPolygonsLab(self.label.symbol,labelpls)
        #else:
        #    feature = dataset.GetNextFeature()
        #    geomreftype = layerGeomT
        #    pen = getPanSymbol(self.symbol)#wx.BLACK_PEN
        #    brush = getBrushSymbol(self.symbol)#wx.RED_BRUSH
        #    self.symsize = getSizeSymbol(self.symbol)
        #    dc.SetPen(pen)
        #    dc.SetBrush(brush)
        #    drawFun = self.featureDrawMap[geomreftype]
        #    while feature:
        #        geomref = feature.GetGeometryRef()
        #        drawFun(dc,geomref,pen,brush,scale,x,y,mx,my)
        #        feature = dataset.GetNextFeature()
        #thisfont.GetPointSize()

        end = time.time()
        debug('spend time:%s,%s',end-star,self.ctime)
        
    def _ConvertPoints(self, xs, ys , scale, x, y,mx,my):
        """批量转换点位置从地理位置到图板位置
        """
        return (xs-self.minx-x)*scale+mx, \
                    (self.maxy-ys-y)*scale+my
        
    def _GetPoints(self,georef,scale,x,y,mx,my):
        """获取Feature几何形状中的所有点xy列表
        @type georef: GDAL Geometry
        @param georef: 要绘制的几何形状
        @type scale: float
        @param scale: XY需要缩放的倍数
        @type x,y: number
        @param x,y: 返回图像的X,Y
        @type mx,my: number
        @param mx,my: 在地图矩形中的图像的X,Y
        """
        pointcount = georef.GetPointCount()
        piarr = range(pointcount)
        xs = reshape(array(map(lambda i: georef.GetX(i),piarr),Float),(-1,1))
        ys = reshape(array(map(lambda i: georef.GetY(i),piarr),Float),(-1,1))
        xs,ys = self._ConvertPoints(xs,ys,scale,x,y,mx,my)
        #xs,ys = (xs-self.minx-x)*scale+mx, \
                #            (self.maxy-ys-y)*scale+my
        points = concatenate((xs,ys),1)
        return points

    def __DrawLine(self,dc,georef,pen,brush,scale,x,y,mx,my):
        """绘制线
        @type georef: GDAL Geometry
        @param georef: 要绘制的几何形状
        @type scale: float
        @param scale: XY需要缩放的倍数
        @type x,y: number
        @param x,y: 返回图像的X,Y
        @type mx,my: number
        @param mx,my: 在地图矩形中的图像的X,Y
        """
        #star = time.time()
        points = self._GetPoints(georef,scale,x,y,mx,my)
        #end = time.time()
        #self.ctime += (end-star)
        dc.DrawLines(points,0,0)
        if self.label and len(self.labstrnow)>0:
            dcpsLine = CreateLineString(points)
            dcRect = GetGeoRectGeometry(self.dcrect)
            dcmLine = dcRect.Intersection(dcpsLine)
            if dcmLine.GetGeometryType()==ogr.wkbLineString:
                lp = LineStringParser(dcmLine)
                x,y = lp.GetMidPoint()
                self.labells.append([lp,self.labstrnow])
            else:
                gc = dcmLine.GetGeometryCount()
                for i in range(gc):
                    g = dcmLine.GetGeometryRef(i)
                    lp = LineStringParser(g)
                    self.labells.append([lp,self.labstrnow])
        
    def __DrawPoint(self,dc,georef,pen,brush,scale,x,y,mx,my):
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
        #star = time.time()
        points = self._GetPoints(georef,scale,x,y,mx,my)
        #dc.SetBrush(brush)
        dc.DrawCirclePoint(points[0],self.symsize)
        #dc.SetPen(wx.Pen(wx.GREEN,3))
        #dc.DrawPointList(points)
        #end = time.time()
        #self.ctime = self.ctime+end-star
        point = points.astype(Int)[0]
        if self.label and len(self.labstrnow)>0:
            self.labelps.append([[point[0],point[1]],self.labstrnow])  
            #self.labstrp.append(self.labstrnow)
        
    def __DrawPolygon(self,dc,georef,pen,brush,scale,x,y,mx,my):
        """绘制多边形
        @type georef: GDAL Geometry
        @param georef: 要绘制的几何形状
        @type scale: float
        @param scale: XY需要缩放的倍数
        @type x,y: number
        @param x,y: 返回图像的X,Y
        @type mx,my: number
        @param mx,my: 在地图矩形中的图像的X,Y
        """
        #star = time.time()
        georef.CloseRings()
        if georef.GetGeometryCount()>1:
            oldpen = dc.GetPen()
            dc.SetPen(wx.TRANSPARENT_PEN)
        geom = georef.GetGeometryRef(0)
        points = self._GetPoints(geom,scale,x,y,mx,my)
        if points[0] != points[-1]:
            points = concatenate([points,[points[0]]])
        for i in range(georef.GetGeometryCount()):
            if i ==0:
                continue
            path = georef.GetGeometryRef(i)
            ppoints = self._GetPoints(path, scale, x,y,mx,my)
            points = concatenate([points,ppoints])
            if points[0] != points[-1]:
                points = concatenate([points,[points[0]]])
        dc.DrawPolygon(points,0,0)
        if georef.GetGeometryCount()>1:
            dc.SetPen(oldpen)
            for i in range(georef.GetGeometryCount()):
                geom = georef.GetGeometryRef(i)
                points = self._GetPoints(geom,scale,x,y,mx,my)
                dc.DrawLines(points,0,0)
        #end = time.time()
        #self.ctime = self.ctime+end-star
        if self.label and len(self.labstrnow)>0:
            dcpsPolygon = CreatePolygon(points)
            fu = FontUtils(self.label.symbol)
            w,h = fu.GetFontSize(self.labstrnow)
            dcRect = GetGeoRectGeometry(self.dcrect)
            dcmPolygon = dcRect.Intersection(dcpsPolygon)
            if dcmPolygon.GetGeometryType()==ogr.wkbPolygon:
                e = dcmPolygon.GetEnvelope()
                if math.fabs(e[0]-e[1])<w or math.fabs(e[2]-e[3])<h:
                    return
                cid = GetBetterCentroid(dcmPolygon,(w,h))
                cidx,cidy = cid.GetX(),cid.GetY()
                self.labelpls.append([[int(cidx),int(cidy)],self.labstrnow])
            else:
                gc = dcmPolygon.GetGeometryCount()
                for i in range(gc):
                    g = dcmPolygon.GetGeometryRef(i)
                    e = g.GetEnvelope()
                    if math.fabs(e[0]-e[1])<w or math.fabs(e[2]-e[3])<h:
                        continue
                    #cid = g.Centroid()
                    cid = GetBetterCentroid(g,(w,h))
                    cidx,cidy = cid.GetX(),cid.GetY()
                    self.labelpls.append([[int(cidx),int(cidy)],self.labstrnow])
        
    def __DrawLines(self,dc,georef,pen,brush,scale,x,y,mx,my):
        """绘制多线
        @type georef: GDAL Geometry
        @param georef: 要绘制的几何形状
        @type scale: float
        @param scale: XY需要缩放的倍数
        @type x,y: number
        @param x,y: 返回图像的X,Y
        @type mx,my: number
        @param mx,my: 在地图矩形中的图像的X,Y
        """
        sublinecount = georef.GetGeometryCount()
        for i in range(sublinecount):
            self.__DrawLine(dc,georef.GetGeometryRef(i), \
                pen,brush,scale,x,y,mx,my)
            
    def __DrawPoints(self,dc,georef,pen,brush,scale,x,y,mx,my):
        """绘制多点
        @type georef: GDAL Geometry
        @param georef: 要绘制的几何形状
        @type scale: float
        @param scale: XY需要缩放的倍数
        @type x,y: number
        @param x,y: 返回图像的X,Y
        @type mx,my: number
        @param mx,my: 在地图矩形中的图像的X,Y
        """
        sublinecount = georef.GetGeometryCount()
        for i in range(sublinecount):
            self.__DrawPoint(dc,georef.GetGeometryRef(i), \
                pen,brush,scale,x,y,mx,my)
            
    def __DrawPolygons(self,dc,georef,pen,brush,scale,x,y,mx,my):
        """绘制多多边形
        @type georef: GDAL Geometry
        @param georef: 要绘制的几何形状
        @type scale: float
        @param scale: XY需要缩放的倍数
        @type x,y: number
        @param x,y: 返回图像的X,Y
        @type mx,my: number
        @param mx,my: 在地图矩形中的图像的X,Y
        """
        sublinecount = georef.GetGeometryCount()
        for i in range(sublinecount):
            self.__DrawPolygon(dc,georef.GetGeometryRef(i), \
                pen,brush,scale,x,y,mx,my)

class HLLayerRender(VectorRender):
    """选择高亮feaure绘制的画板
    """
    def __init__(self,layer):
        VectorRender.__init__(self,layer)
        self.where = ""
        self.codec = None

    def Draw(self,dc,wprect,wgrect):
        """绘制图层，往后的子类都要继承这个方法
        @type dc: wxDC
        @param dc: 绘制可用的DC
        @type wprect: L{geosings.core.GeoRect}
        @param wprect: DC的范围，主要用于分辨率判断
        @type wgrect: L{geosings.core.GeoRect}
        @param wgrect: 地图的地理范围
        """
        try:
            x,y,w,h,bw,bh,mx,my = self.layer.CacDrawArgs(wprect,wgrect)
            scale = bh*1.0/h
        except Exception, args:
            err('CacDrawArgs false:',args)
            return
        self.dcrect = wprect
        dataset = self.layer.DataSet()
        exgeom = GetGeoRectGeometry(wgrect)
        log("Attribute Filter:"+self.where)
        self.layer.SetAttributeFilter(self.where,self.codec)
        dataset.SetSpatialFilter(exgeom)
        featurecount = dataset.GetFeatureCount()
        dataset.ResetReading()
        
        gc = GDC(dc)#换到GC,支持透明

        layerGeomT = dataset.GetLayerDefn().GetGeomType()
        self.symbol = CreateHLSymbol(layerGeomT)
        pen = getPanSymbol(self.symbol)#wx.BLACK_PEN
        brush = getBrushSymbol(self.symbol)#wx.RED_BRUSH
        self.symsize = getSizeSymbol(self.symbol)
        gc.SetPen(pen)
        gc.SetBrush(brush)
        self.minx = self.layer.DataGeoExt.GetLeft()
        self.maxy = self.layer.DataGeoExt.GetTop()
            
        #开始循环绘制Feature
        feature = dataset.GetNextFeature()
        while feature:
            geomref = feature.GetGeometryRef()
            geomreftype = geomref.GetGeometryType()
            drawFun = self.featureDrawMap[geomreftype]
            drawFun(gc,geomref,pen,brush,scale,x,y,mx,my)
            feature = dataset.GetNextFeature()
        self.layer.SetAttributeFilter("")

    def SetWhereFilter(self,where,codec=None):
        self.where = where
        self.codec = codec

    def SetSpatialFilter(self, geom):
        pass

class FeaturesRender(VectorRender):
    """要素的画板
    """
    def __init__(self,features):
        """初始化画板
        @type features: list
        @param features: 要绘制的要素列表
        """
        from geosings.ui.PyMainPanel import GetMainPanel
        layer = GetMainPanel().canvas.map.GetLayers()[0]
        VectorRender.__init__(self,layer)
        self.features = features
        self.wink = 1
        self.aimFoo = None
        self.symbols = {
            ogr.wkbPoint:self.__InitHLSymbol(ogr.wkbPoint),
            ogr.wkbMultiPoint:self.__InitHLSymbol(ogr.wkbMultiPoint),
            ogr.wkbLineString:self.__InitHLSymbol(ogr.wkbLineString),
            ogr.wkbMultiLineString:self.__InitHLSymbol(ogr.wkbMultiLineString),
            ogr.wkbPolygon:self.__InitHLSymbol(ogr.wkbPolygon),
            ogr.wkbMultiPolygon:self.__InitHLSymbol(ogr.wkbMultiPolygon)
        }

    def SetWink(self, winknum):
        """设置闪烁次数
        @type winknum: int
        @param winknum: 闪烁次数
        """
        self.wink = winknum

    def GetHLSymbol(self,layerGeomT):
        """获取高亮样式的样式，画笔刷子等
        """
        sym = self.symbols[layerGeomT]
        return sym[0],sym[1],sym[2],sym[3]

    def __InitHLSymbol(self,layerGeomT):
        """初始化指定类型的高亮样式
        """
        symbol = CreateHLSymbol(layerGeomT)
        pen = getPanSymbol(symbol)#wx.BLACK_PEN
        brush = getBrushSymbol(symbol)#wx.RED_BRUSH
        symsize = getSizeSymbol(symbol)
        return [symbol,pen,brush,symsize]

    def BindAimFoo(self, foo):
        self.aimFoo = foo

    def Draw(self,dc,wprect,wgrect):
        """绘制图层，往后的子类都要继承这个方法
        @type dc: wxDC
        @param dc: 绘制可用的DC
        @type wprect: L{geosings.core.GeoRect}
        @param wprect: DC的范围，主要用于分辨率判断
        @type wgrect: L{geosings.core.GeoRect}
        @param wgrect: 地图的地理范围
        """
        try:
            x,y,w,h,bw,bh,mx,my = self.layer.CacDrawArgs(wprect,wgrect)
            scale = bh*1.0/h
        except Exception, args:
            err('CacDrawArgs false:',args)
            return

        self.minx = self.layer.DataGeoExt.GetLeft()
        self.maxy = self.layer.DataGeoExt.GetTop()

        if self.aimFoo is not None:
            ext = RectExt()
            for feature in self.features:
                r = feature.GetGeometryRef().GetEnvelope()
                ext.AddRect(GeoRect(r[0],r[2],r[1],r[3]))
            #gmidx,gmidy = ext.GetExt().GetMiddlePoint()
            tr = ext.GetExt()
            left,top = tr.GetLeft(),tr.GetTop()
            right,bottom = tr.GetRight(),tr.GetBottom()
            lx,ty = self._ConvertPoints(left,top,scale,x,y,mx,my)
            rx,by = self._ConvertPoints(right,bottom,scale,x,y,mx,my)
            xsize,ysize = rx-lx,int(math.fabs(by-ty))
            #self.aimFoo([midx,midy])
            self.aimFoo([lx,ty,xsize,ysize])
        

        dc.SetLogicalFunction(wx.XOR)
        for i in range(self.wink):
            #开始循环绘制Feature
            for feature in self.features:
                geomref = feature.GetGeometryRef()
                geomreftype = geomref.GetGeometryType()
                symbol,pen,brush,symsize = self.GetHLSymbol(geomreftype)
                dc.SetPen(pen)
                dc.SetBrush(brush)
                drawFun = self.featureDrawMap[geomreftype]
                drawFun(dc,geomref,pen,brush,scale,x,y,mx,my)
        dc.SetLogicalFunction(wx.COPY)

class RasterRender(LayerRender):
    """栅格图层的画板
    """
    def __init__(self,layer):
        """初始化画板
        @type layer: L{geosings.core.Layer}
        @param layer: 初始化画板的图层
        """
        self.layer = layer

    def Draw(self,dc,wprect,wgrect):
        """绘制图层
        @type dc: wxDC
        @param dc: 绘制可用的DC
        @type wprect: L{geosings.core.GeoRect}
        @param wprect: DC的范围，主要用于分辨率判断
        @type wgrect: L{geosings.core.GeoRect}
        @param wgrect: 地图的地理范围
        """
        try:
            x,y,w,h,bw,bh,mx,my = self.layer.CacDrawArgs(wprect,wgrect)
        except Exception, args:
            err('CacDrawArgs false:',args)
            return
        for i in range(3):
            if self.layer.DataSet().RasterCount < 3:
                band = self.layer.DataSet().GetRasterBand(1)
            else: band = self.layer.DataSet().GetRasterBand(i+1)
            if w>0 and h>0:
                tdata = band.ReadAsArray(int(x),int(y),
                            int(w),int(h),int(bw),int(bh))
                if i==0:
                    data = tdata
                    data.shape = (-1,1)
                else :
                    tdata.shape = (-1,1)
                    data = concatenate((data,tdata),1)
        if bw>0 and bh>0: 
            data = data.astype(Int8)
            img = wx.EmptyImage(bw,bh)
            img.SetData(data.tostring())
            bmp = img.ConvertToBitmap()
            dc.DrawBitmap(bmp,mx,my,False)


