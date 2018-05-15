# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.7.4; version:1; 创建
"""
该模块定义栅格影像一些特殊的操作
"""

import gdal,Image,os,math
import Numeric as Num
from geosings.core.Layer import *
from geosings.core.RasterUtil import *

class RasterSplitter:
    """栅格图像分割类
    """
    def __init__(self, rasLayer):
        """初始化
        @type rasLayer: str,Layer
        @param rasLayer: 要分割的栅格图层
        """
        if type(rasLayer) == str:
            self.rasLayer = Layer.Open(rasLayer)
        else:
            self.rasLayer = rasLayer
        self.dataset = self.rasLayer.DataSet()
        self.w = self.dataset.RasterXSize
        self.h = self.dataset.RasterYSize
        self.bandcount = self.dataset.RasterCount

    def Split(self, opath, blockw=256, blockh=256):
        """分割图像
        @type opath: str
        @param opath: 要输出分割好的图像的路径
        @type blockw: int
        @param blockw: 要分割的瓦片的宽
        @type blockh: int
        @param blockh: 要分割的瓦片的高
        """
        xblockcount = int(ceil(self.w*1.0/blockw))
        yblockcount = int(ceil(self.h*1.0/blockh))
        #print xblockcount, self.w*1.0/blockw,yblockcount, self.h*1.0/blockh
        for y in range(yblockcount):
            for x in range(xblockcount):
                ofilename = os.path.join(opath,'x%dy%d.png' % (x,y))
                begx,begy = blockw*x,blockh*y
                width,height = blockw,blockh
                data = ReadRaster(self.dataset,begx,begy,width,height)
                PILSaveData(data,ofilename)

                step = (y*xblockcount+x)*100.0/(yblockcount*xblockcount) 
                if not (step)%10:
                    print step,"% ..."

def ResizeRaster(raster,scale, ogtif ):
    """栅格图像缩放处理函数
    """
    width = raster.RasterXSize
    height = raster.RasterYSize
    swidth = int(width*scale)
    sheight = int(height*scale)
    driver = gdal.GetDriverByName("GTiff")
    tods = driver.Create(ogtif,swidth,sheight,3,options=["INTERLEAVE=PIXEL"])
    datas = raster.ReadRaster(0,0,width,height,swidth,sheight)
    #arr = Num.fromstring(datas, Num.Int8)
    bandlist = Num.arange(raster.RasterCount)+1
    tods.WriteRaster(0,0,swidth,sheight,datas,#arr.tostring(),
            swidth,sheight,band_list=bandlist.tolist())

if __name__=="__main__":
    RasterSplitter("e:/gisdata/gtif/fj_tm.tif").Split("d:/gisdata/fj")
    #raster = gdal.Open("e:/gisdata/gtif/fj_tm.tif")
    #ResizeRaster(raster,1.0/4,"d:/tmp/fj_tm_s2.tif") 

