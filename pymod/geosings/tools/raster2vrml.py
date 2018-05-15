# -*- coding: utf-8 -*-
"""进行DEM到VRML的转换
"""
import gdal
import math,os
from Numeric import *
from geosings.core.Layer import Layer
from geosings.core.system import *

class Raster2Vrml:
    def __getShape(self, shape):
        """包装成Shape节点
        """
        return "Shape{\n%s\n}" % shape

    def __getElevationGrid(self, heights,**keymap):
        """包装成ElevationGrid节点
        """
        pstr = ["%s %s" % (k,str(v)) for k,v in keymap.items()]
        prep = "\n".join(pstr)+"\n"
        elevs = "\n\t".join([", ".join([str(j) for j in i]) for i in heights])
        h = "height [\n\t%s\n]" % elevs
        context = prep+h
        return "geometry ElevationGrid{\n%s\n}" % context

    def __getCoorArray(self, w,h):
        """包装成TexCoord节点的纹理映射坐标
        """
        warr = arange(0.0, 1.0, 1.0/(w+1))[1:]
        harr = arange(1.0, 0.0, -1.0/(h+1))[1:]
        points = "\n\t".join([",".join(["%s %s" % (str(i),str(j)) for i in warr])for j in harr])
        return "point[\n\t%s\n]" % points

    def __getTexCoord(self, w,h):
        """包装成TexCoord节点
        """
        points = self.__getCoorArray(w,h)
        return "TextureCoordinate{\n%s\n}" % points

    def __getAppearance(self, imgname):
        """包装材质节点
        """
        return """
        appearance DEF DEMCOLOR Appearance {
            material Material {
                diffuseColor 0.1843 0.5 0.2
            }
            texture ImageTexture {
                url ["%s"] 
                repeatS TRUE
                repeatT TRUE
            }
        }
        """ % imgname

    def Convert(self, dem, outputpath=".", name="dem",
            zipByWH='w', zipv=300, convimg=False):
        """转换dem为vrml
        @type dem: str | RasterDataSet 
        @param dem: 输出路径
        @type convimg: bool
        @param convimg: 要不要转换图像？
        """
        print type(dem),dem
        if type(dem)==str or type(dem)==unicode:#如果是路径就打开dem
            ds = gdal.Open(dem)
        elif issubclass(dem.__class__, Layer): #如果是RasterLayer就获取DataSet
            ds = dem.DataSet()
        else: #如果是数据集就直接用
            ds = dem

        #读取波段信息
        band = ds.GetRasterBand(1)
        #print band.XSize,band.YSize
        trans = ds.GetGeoTransform()
        bandXSize = band.XSize
        bandYSize = band.YSize

        toSIZE = choose(zipByWH=='w',bandXSize,bandYSize)
        if toSIZE>zipv:#压缩像素到最大300个像素，太大了浏览器跑不动
            scale = zipv*1.0/toSIZE
            bandXSize = int(bandXSize*scale)
            bandYSize = int(bandYSize*scale)
        else:scale=1

        #print bandXSize,bandYSize
        xres = trans[1]/scale
        yres = math.fabs(trans[5])/scale
        #print xres,yres
        #读取波段数据
        elevs = band.ReadAsArray(0,0,band.XSize,band.YSize,bandXSize,bandYSize)


        #开始进行转换
        imgname = os.path.join(outputpath, name+".jpg")
        vrname = os.path.join(outputpath, name+".wrl")
        if os.access(vrname,os.R_OK):os.remove(vrname)

        #打开文件输入vrml文本
        file = open(vrname,'w')
        file.write("#VRML V2.0 utf8\n")
        appeartext = self.__getAppearance(imgname)
        elevtext = self.__getElevationGrid(elevs,
                xDimension=bandXSize,
                zDimension= bandYSize,
                xSpacing=xres,
                zSpacing=yres,
                solid='TRUE',
                creaseAngle=0.0,
                texCoord = self.__getTexCoord(bandXSize,bandYSize))
        shapetext = "\n".join([appeartext,elevtext])
        context = self.__getShape(shapetext)
        file.write(context)
        file.close()

        #拷贝图像成jpg
        #这里有一些问题，如果不是Byte的数据类型就会出错。
        #若出错，可以用其他的软件手动改，或者再写一段代码
        #其实这些都没有关系，有了映射坐标，随便什么图都好，要的就是那张皮。
        #不过支持的格式有限，只有jpg，gif等少数格式
        if not convimg:
            return
        try:
            if os.access(imgname,os.R_OK):os.remove(imgname)
            format = "jpeg"
            driver = gdal.GetDriverByName( format )
            dst_ds = driver.CreateCopy(name+".jpg",ds)
        except:
            print _("covert image failure")

if __name__=="__main__":
    #ras2vrml('J:/arcgis/ArcTutor/Catalog/Yellowstone/dem30', True);
    #ras2vrml('J:/gisdata/gtif/dem.tif', True);
    Raster2Vrml().Convert("E:/GISdata/gtif/asp.tif", "e:/gisdata",
            "spotdem", 'w', 200)
