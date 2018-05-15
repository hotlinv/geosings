#!python
# -*- coding: utf-8 -*-
"""
把一张图片弄成文件形式的金字塔

$ linux_23 $ 2006.10.14 $ 创建
"""

import Image
import gdal
import os.path

from Numeric import *
from geosings.core.system import choose

class RasterPyramidBuilder:
    """栅格金字塔的建立类
    """
    def __init__(self,fileinput,outputdir):
        """初始化类
        @type fileinput: str
        @param fileinput: 输入图层的名称
        @type outputdir: str
        @param outputdir: 输出金字塔文件夹
        """
        self.dataset = gdal.Open(fileinput)
        self.bandcount = self.dataset.RasterCount
        self.outputdir = outputdir

    def __GetBlockCount(self,w,h):
        """获取这一层图层一共有多少个瓦片
        @type w,h: int
        @param w,h: 图层有多少宽高
        @rtype: list
        @return: 返回横向和纵向有多少个瓦片
                    - 横向瓦片个数
                    - 纵向瓦片个数
        """
        bxcount = choose(w%self.blockw==0,w/self.blockw,w/self.blockw+1)
        bycount = choose(h%self.blockh==0,h/self.blockh,h/self.blockh+1)
        return bxcount,bycount

    def __CacPyH(self,w,h):
        """计算金字塔高
        @type w,h: int
        @param w,h: 图层宽高
        @rtype: int
        @return: 金字塔高
        """
        nowpyh = 1
        noww,nowh = w,h
        while (1):
            bxcount,bycount = self.__GetBlockCount(noww,nowh)
            if bxcount==1 or bycount == 1:
                break
            noww/=2;nowh/=2;nowpyh+=1
        return nowpyh

    def __GetEmptyBlock(self,bandcount,w,h):
        """获取空瓦片数据
        @type bandcount: int
        @param bandcount: 图层波段数
        @type w,h: int
        @param w,h: 瓦片宽高
        @rtype: list
        @return: 瓦片数据
        """
        return zeros((bandcount,w,h),Int8)

    def __FromGeoPGetImageP(self,scale,geox,geoy):
        """由地理点获取对应图像点
        @type scale: number
        @param scale: 缩放倍率
        @type geox,geoy: number
        @param geox,geoy: 地理坐标
        @rtype: list
        @return: 图像点xy的列表
        """
        imgy = (self.gt[0]-self.gt[3]+geoy-geox)/(self.gt[5]-self.gt[2])
        imgx = geox-self.gt[0]-imgy*self.gt[2]
        return imgx,imgy

    def __FromImgPGetGeoP(self,scale,imgx,imgy):
        """由图像点获取对应地理点
        @type scale: number
        @param scale: 缩放倍率
        @type imgx,imgy: number
        @param imgx,imgy: 图像坐标
        @rtype: list
        @return: 地理点xy的列表
        """
        geox = self.gt[0]+imgx*self.gt[1]+imgy*self.gt[2]
        geoy = self.gt[3]+imgx*self.gt[4]+imgy*self.gt[5]
        return geox,geoy

    def __ReadBlockData(self,scale,x,y):
        """获取瓦片数据
        @type scale: number
        @param scale: 缩放倍率
        @type x,y: int
        @param x,y: 瓦片的位置
        @rtype: list
        @return: 瓦片数据
        """
        print 'now at:',x,y,"   ",
        orixnow,oriynow = self.__FromGeoPGetImageP(scale,self.origeo[0],
                self.origeo[1])#现在初始原点的位置
        blockwnow,blockhnow = self.blockw/scale,self.blockh/scale
        #计算要读取的瓦片在原始数据中的范围。
        tmpx,tmpy = orixnow+x*blockwnow,oriynow+y*blockhnow
        tmpx2,tmpy2 = tmpx+blockwnow,tmpy+blockhnow
        left,right,top,bottom = 0,0,0,0 #需要补足的地方
        if tmpx<0:
            left = int(-tmpx*scale)#需要在左边补足tmpx的列
            tmpx = 0
        if tmpy<0:
            top = int(-tmpy*scale)#需要在上面补足tmpy的行
            tmpy = 0
        if tmpx2>self.dataset.RasterXSize:
            #需要在右边补足...的列
            right = int((tmpx2-self.dataset.RasterXSize)*scale)
            tmpx2 = self.dataset.RasterXSize
        if tmpy2>self.dataset.RasterYSize:
            #需要在底下补足...的行
            bottom = int((tmpy2-self.dataset.RasterYSize)*scale)
            tmpy2 = self.dataset.RasterYSize
        readw,readh = int(tmpx2-tmpx),int(tmpy2-tmpy)
        readx,ready = int(tmpx),int(tmpy)
        bufw,bufh = self.blockw-left-right,self.blockh-top-bottom
        data = None
        if readw!=0 or readh !=0:
            bands = [self.dataset.GetRasterBand(bi+1) for bi in range(self.dataset.RasterCount)]
            #print readx,ready,readw,readh,bufw,bufh,left,right,top,bottom
            datas = [b.ReadAsArray(readx,ready,readw,readh,bufw,bufh) for b in bands]
            if top!=0:
                topdata = zeros((top,datas[0].shape[1]))
                datas = [concatenate((topdata,i)) for i in datas]
            if bottom!=0:
                botdata = zeros((bottom,datas[0].shape[1]))
                datas = [concatenate((i,botdata)) for i in datas]
            if left !=0:
                leftdata = zeros((datas[0].shape[0],left))
                datas = [concatenate((leftdata,i),1) for i in datas]
            if right!=0:
                rightdata = zeros((datas[0].shape[0],right))
                datas = [concatenate((i,rightdata),1) for i in datas]
            #组织成Image识别的形式
            datas = [reshape(i,(-1,1)) for i in datas]
            data = concatenate(datas,1).astype(Int8)
        else:
            #print 'empty'
            data = self.__GetEmptyBlock(3,self.blockw,self.blockh)
        print
        return data

    def __SaveBlockData(self,data,pyh,x,y):
        """保存瓦片数据
        @type data: list
        @param data: 要保存的数据
        @type pyh: int
        @param pyh: 金字塔高度
        @type x,y: int
        @param x,y: 瓦片位置
        """
        filename = 'py%d-x%d-y%d.png' % (pyh,x,y)
        Image.fromstring('RGB',(self.blockw,self.blockh),data.tostring()) \
                .save(os.path.join(self.outputdir,filename))

    def BuildFilePyramid(self,pyheight=0,blockw=128,blockh=128,
            orix=0,oriy=0):
        """建立文件金字塔
        @type pyheight: int
        @param pyheight: 金字塔高
        @type blockw,blockh: int
        @param blockw,blockh: 瓦片的宽高
        @type orix,oriy: int
        @param orix,oriy: 瓦片便宜
        """
        print 'begin'
        self.orix,self.oriy = orix,oriy
        self.blockw = blockw
        self.blockh = blockh
        self.width = self.dataset.RasterXSize-orix
        self.height = self.dataset.RasterYSize-oriy
        self.realext = (-orix,-oriy,
            self.width,self.height)
        geotf = self.dataset.GetGeoTransform()
        self.gt = geotf
        self.geoext = [geotf[0],geotf[3],
                geotf[0]+geotf[1]*self.width+geotf[2]*self.height,
                geotf[3]+geotf[4]*self.width+geotf[5]*self.height]
        self.origeo = [
                geotf[0]+geotf[1]*self.orix+geotf[2]*self.oriy,
                geotf[3]+geotf[4]*self.orix+geotf[5]*self.oriy,
                ]
        self.baseBlockGeoSize = [
                geotf[1]*self.blockw, geotf[5]*self.blockh,
                ]
        self.pyheight = self.__CacPyH(self.width,self.height)
        if pyheight>0 and pyheight<self.pyheight:#计算
            self.pyheight = pyheight

        print "will build pyheight:",self.pyheight

        noww,nowh = self.width,self.height
        scale = 1.0
        for pyh in range(self.pyheight):
            print 'build py',pyh
            #开始建立金字塔
            #计算读取范围
            bxcount,bycount = self.__GetBlockCount(noww,nowh)
            for y in range(bycount):
                for x in range(bxcount):
                    data = self.__ReadBlockData(scale,x,y)
                    self.__SaveBlockData(data,pyh,x,y)
            #保存坐标信息
            prjfname = os.path.join(self.outputdir,"py%d.info" % pyh);
            f = open(prjfname,'w')
            geox,geoy = self.origeo
            geow = self.baseBlockGeoSize[0]*bxcount/scale
            geoh = self.baseBlockGeoSize[1]*bycount/scale
            context = ["bxcount:%d" % bxcount,"bycount:%d" % bycount,
                    "geoext:%f,%f,%f,%f" % (geox,geoy,geox+geow,geoy+geoh)]
            f.write('\n'.join(context))
            f.close()
            #循环
            noww/=2;nowh/=2
            scale/=2

        #单独建立一个空block 
        data = self.__GetEmptyBlock(3,self.blockw,self.blockh)
        Image.fromstring('RGB',(self.blockw,self.blockh),data.tostring()) \
                .save(os.path.join(self.outputdir,'empty.png'))
        print 'success'

if __name__=="__main__":
    builder = RasterPyramidBuilder('J:/gisdata/gtif/zp_tm.tif',
            'J:/gisdata/gsseyedata/')
    builder.BuildFilePyramid()

