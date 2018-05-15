# -*- coding: utf-8 -*-
"""
该模块定义栅格操作辅助

 - writer:linux_23; create: 2007.7.2; version:1; 创建
"""
import gdal,Image,os,math
import Numeric as Num
from geosings.core.Layer import *

def RRGGBB2RGBRGB(RRGGBB):
    """把RRRGGGBBB格式的数据变成RGBRGB格式
    @type RRGGBB: Numeric array
    @param RRGGBB: RRRGGGBBB格式的数组
    @rtype: Numeric array
    @return: RGBRGBRGB格式的数组
    """
    return Num.swapaxes(Num.swapaxes(RRGGBB,0,1),1,2)

def RGBRGB2RRGGBB(RGBRGB):
    """把RGBRGB格式的数据变成RRGGBB格式
    @type RGBRGB: Numeric array
    @param RGBRGB: RGBRGBRGB格式的数组
    @rtype: Numeric array
    @return: RRRGGGBBB格式的数组
    """
    return Num.swapaxes(Num.swapaxes(RRGGBB,1,2),0,1)

def PILSaveData(data, path):
    """用PIL来保存栅格数据
    @type data: list
    @param data: 要保存的数据
    @type path: str
    @param path: 要保存图片的位置
    """
    #print data ,data.shape
    size = data.shape
    h,w = size[0],size[1]
    Image.fromstring('RGB',(w,h),data.tostring()).save(path)
    #Image.fromstring('L',(h,w),data.tostring()).save(path)

def ReadRaster(raster, x, y, w, h):
    """读取栅格数据（用来保证越界不会出错）
    @type raster: gdal.RasterDataset
    @param raster: 数据集
    @type x:int
    @type y:int
    @type w:int
    @type h: int
    @param x,y,w,h: 读取栅格的矩形大小
    """
    rasw,rash = raster.RasterXSize,raster.RasterYSize
    bandcount = raster.RasterCount
    begx,begy,width,height = x,y,w,h
    exwr,exwl,exhb,exht = 0,0,0,0 #超过图像范围的行列
    if x<0:
        begx = 0
        exwl = -x
        width -= exwl
    if y<0:
        begy = 0
        exht = -y
        height -= exht
    if x+w>rasw:
        exwr = x+w-rasw
        width = rasw-begx
    if y+h>rash:
        exhb = y+h-rash
        height = rash-begy
    print begx,begy,width,height
    data = raster.ReadAsArray(begx,begy,width,height)
    datatype = data.typecode()
    data = RRGGBB2RGBRGB(data)

    #进行数组的扩展和补充
    if exwl>0 and exwr>0:
        data1 = Num.zeros((height,exwl,bandcount),datatype) 
        data2 = Num.zeros((height,exwr,bandcount),datatype) 
        data = Num.concatenate((data1,data,data2),1)
    elif exwl>0:
        data1 = Num.zeros((height,exwl,bandcount),datatype) 
        data = Num.concatenate((data1,data),1)
    elif exwr>0:
        data2 = Num.zeros((height,exwr,bandcount),datatype) 
        data = Num.concatenate((data,data2),1)

    if exht>0 and exhb>0:
        data1 = Num.zeros((exht,w,bandcount),datatype) 
        data2 = Num.zeros((exhb,w,bandcount),datatype) 
        data = Num.concatenate((data1,data,data2))
    elif exht>0:
        data1 = Num.zeros((exht,w,bandcount),datatype) 
        data = Num.concatenate((data1,data))
    elif exhb>0:
        data2 = Num.zeros((exhb,w,bandcount),datatype) 
        data = Num.concatenate((data,data2))

    return data

if __name__=="__main__":
    ds = gdal.Open("e:/gisdata/gtif/sd.tif")
    data = ReadRaster(ds, -100, -100, 1300, 1300)
    PILSaveData(data, "d:/gisdata/sd.tif")
