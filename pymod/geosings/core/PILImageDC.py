# -*- coding: utf-8 -*-
import Image, ImageDraw
import sys,math
import ogr
from Numeric import *

class PILByteImageDC:
    def __init__(self):
        FeatureDrawMap = {
            #ogr.wkbPoint:self.__DrawPoint,
            #ogr.wkbMultiPoint:self.__DrawPoints,
            ogr.wkbLineString:self.__DrawLine,
            ogr.wkbMultiLineString:self.__DrawLines,
            ogr.wkbPolygon:self.__DrawPolygon,
            ogr.wkbMultiPolygon:self.__DrawPolygons
            }
        self.featureDrawMap = FeatureDrawMap
        self.fill = 255
        self.outline = None
        self.outputGeoInfo = False
        self.colorMode = 'L'
        self.im = None

    def DrawAGeoRef(self,georef,width,height,minx,maxy,scale):
        self.minx = minx
        self.maxy = maxy
        self.scale = scale

        self.im = Image.new(self.colorMode,(width,height),0)
        self.draw = ImageDraw.Draw(self.im)

        geomreftype = georef.GetGeometryType()
        drawFun = self.featureDrawMap[geomreftype]
        drawFun(georef)

        del self.draw

        #self.im.save("f:/gisdata/kk.png", 'png')

    def __GetPoints(self,georef):
        pointcount = georef.GetPointCount()
        xs,ys = [],[]
        for i in range(pointcount):
            xs.append(georef.GetX(i))
            ys.append(georef.GetY(i))
        xs = array(xs,Float); ys = array(ys,Float)
        xs = ((xs-self.minx)*self.scale).astype(Float)
        ys = ((self.maxy-ys)*self.scale).astype(Float)
        xs.shape=(-1,1);ys.shape=(-1,1)
        points = concatenate((xs,ys),1)
        return points

    def __DrawLine(self,georef):
        points = self.__GetPoints(georef)
        xys = reshape(points, (1,-1))[0]
        self.draw.line(list(xys),fill=self.fill)

    def __DrawPolygon(self,georef):
        geom = georef.GetGeometryRef(0)
        points = self.__GetPoints(geom)
        xys = reshape(points, (1,-1))[0]
        self.draw.polygon(list(xys),fill=self.fill,outline=self.outline)

    def __DrawLines(self,georef):
        sublinecount = georef.GetGeometryCount()
        for i in range(sublinecount):
            self.__DrawLine(georef.GetGeometryRef(i))

    def __DrawPolygons(self,georef):
        sublinecount = georef.GetGeometryCount()
        for i in range(sublinecount):
            self.__DrawPolygon(georef.GetGeometryRef(i))

class PILImgDC:
    def __init__(self,layer):
        self.layer = layer
        self.features = [layer.GetFeature(i) for i in range(layer.GetFeatureCount())]
        FeatureDrawMap = {
            #ogr.wkbPoint:self.__DrawPoint,
            #ogr.wkbMultiPoint:self.__DrawPoints,
            ogr.wkbLineString:self.__DrawLine,
            ogr.wkbMultiLineString:self.__DrawLines,
            ogr.wkbPolygon:self.__DrawPolygon,
            ogr.wkbMultiPolygon:self.__DrawPolygons
            }
        self.featureDrawMap = FeatureDrawMap
        self.fill = (128,128,128,256)
        self.outline = (0,0,0,256)
        self.outputGeoInfo = True
        self.colorMode = 'RGBA'

    def SetFillColour(self,color):
        self.fill = color

    def SetOutLine(self,outline):
        self.outline = outline

    def SetInputImg(self,imgname):
        self.iimgname = imgname
    def SetOutputGeoInfo(self,output):
        self.outputGeoInfo = output
    def SetColorModel(self,mode):
        self.colorMode = mode
    def __OutputGeoInfo(self,ofname,extent,scale):
        print 'output geoinfo...',
        gt = [1.0/scale,0,0,-1.0/scale,extent[0],extent[3]]
        import os.path
        path,ext = os.path.splitext(ofname)
        filename = path+".tfw"
        f = open(filename,'w')
        f.write("\n".join([str(i) for i in gt]))
        f.close()
        print 'success!'

    def DrawAll(self,conf,ofname,oftype):
        extent = self.layer.GetExtent()
        print extent
        if type(conf)==int:
            width = conf
            geowidth = math.fabs(extent[1]-extent[0])
            geoheight = math.fabs(extent[3]-extent[2])
            height = width/geowidth*geoheight
        elif type(conf)==list:
            gt = conf
            print gt
            tmpgeow = math.fabs(extent[1]-gt[4])
            tmpgeoh = math.fabs(gt[5]-extent[2])
            print tmpgeoh
            width = int(tmpgeow/gt[0])
            tmpgeox2 = gt[4]+width*gt[0]
            height = int(tmpgeoh/-gt[3])
            tmpgeoy2 = gt[5]+height*gt[3]
            extent = [gt[4],tmpgeox2,tmpgeoy2,gt[5]]
            print extent
            geowidth = math.fabs(extent[1]-extent[0])
            geoheight = math.fabs(extent[3]-extent[2])
        self.minx = min(extent[0],extent[1])
        self.maxy = max(extent[3],extent[2])
        self.scale = width/geowidth
        print width,height

        if self.outputGeoInfo:
            try:
                self.__OutputGeoInfo(ofname,extent,self.scale)
            except:
                print 'warning: Output GeoInfo file failse!'

        im = Image.new(self.colorMode,(width,height),(256,256,256,0))
        self.draw = ImageDraw.Draw(im)

        for feature in self.features:
            geomref = feature.GetGeometryRef()
            geomreftype = geomref.GetGeometryType()
            drawFun = self.featureDrawMap[geomreftype]
            drawFun(geomref)

        del self.draw

        im.save(ofname, oftype)

    def __GetPoints(self,georef):
        pointcount = georef.GetPointCount()
        xs,ys = [],[]
        for i in range(pointcount):
            xs.append(georef.GetX(i))
            ys.append(georef.GetY(i))
        xs = array(xs,Float); ys = array(ys,Float)
        xs = (xs-self.minx)*self.scale
        ys = (self.maxy-ys)*self.scale
        xs.shape=(-1,1);ys.shape=(-1,1)
        points = concatenate((xs,ys),1)
        return points

    def __DrawLine(self,georef):
        points = self.__GetPoints(georef)
        xys = reshape(points, (1,-1))[0]
        self.draw.line(xys,fill=self.fill)
    def __DrawPolygon(self,georef):
        geom = georef.GetGeometryRef(0)
        points = self.__GetPoints(geom)
        xys = reshape(points, (1,-1))[0]
        self.draw.polygon(xys,fill=self.fill,outline=self.outline)

    def __DrawLines(self,georef):
        sublinecount = georef.GetGeometryCount()
        for i in range(sublinecount):
            self.__DrawLine(georef.GetGeometryRef(i))

    def __DrawPolygons(self,georef):
        sublinecount = georef.GetGeometryCount()
        for i in range(sublinecount):
            self.__DrawPolygon(georef.GetGeometryRef(i))

if __name__=="__main__":
    #import os.path
    #outputdir = "f:/gisdata"
    #ds = ogr.Open("I:/gisdata/shp/fj_region.shp")
    #layer = ds.GetLayer()

    #dc = PILByteImageDC()
    #dc.SetFillColour((100,100,0,10))
    #dc.SetColorModel('RGB')
    #dc.DrawAGeoRef()
    #dc.DrawAll(300,os.path.join(outputdir,"output.png"),'png')
    pass

