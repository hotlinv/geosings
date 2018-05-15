# -*- coding: utf-8 -*-
"""
这里是管理所有wxDC生成地方

 - writer:linux_23; create:2007.6.14 ; version:1; 创建
"""

import wx, Image, os

class MemDCClass:
    """内存dc
    """
    def __init__(self, width, height):
        """
        """
        self.bitmap = wx.EmptyBitmap(width,height)

        self.dc = wx.MemoryDC()
        self.dc.SelectObject(self.bitmap)
        self.dc.Clear()

    def GetMemDC(self):
        return self.dc

    def SaveImage(self, ofile):
        #self.bitmap.SaveFile(ofile, wx.BITMAP_TYPE_BMP)
        image = self.bitmap.ConvertToImage()
        w = self.bitmap.GetWidth()
        h = self.bitmap.GetHeight()
        data = image.GetData()
        Image.fromstring('RGB',(w,h),data).save(ofile)

    def SaveGeoInfo(self, geoext, ofname):
        w = self.bitmap.GetWidth()
        h = self.bitmap.GetHeight()
        xscale = geoext.GetWidth()*1.0/w
        yscale = geoext.GetHeight()*1.0/h
        gt = [xscale,0,0,-yscale,geoext.GetLeft(),geoext.GetTop()]
        path,ext = os.path.splitext(ofname)
        filename = path+".tfw"
        f = open(filename,'w')
        f.write("\n".join([str(i) for i in gt]))
        f.close()
    
