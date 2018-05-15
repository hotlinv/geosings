# -*- coding: utf-8 -*-
"""该模块定义可以把wkt形式的坐标系统格式成比较好看的形式的类
"""

import re
class WktFormater:
    """格式化坐标系统wkt的类
    """
    def __init__(self,wkt):
        """构造函数
        @type wkt: str
        @param wkt: 要格式化的wkt坐标系统
        """
        wkt = wkt.replace('\n',' ')
        wkt = wkt.replace('\r',' ')
        self.arr = []
        self.__splitwkt(wkt)
        self.arr.reverse()
        #arr = steploop(arr,step)
        #return "\n".join(arr)

    def __splitwkt(self,wkt):
        """分割wkt坐标系统为队列
        @type wkt: str
        @param wkt: 要分割的wkt坐标
        """
        t = re.match('(.+,)(\w+\[.+)',wkt)
        if t is not None:
            gps = t.groups()
            #print gps
            self.arr.append(gps[1])
            self.__splitwkt(gps[0])
        else:
            self.arr.append(wkt)

    def format(self,sign = '\t',step=0):
        """格式化坐标系统
        @type sign: str
        @param sign: 行首分割wkt的字符
        @type step: int
        @param step: 行首分隔符的个数
        """
        for i in range(len(self.arr)):
            self.arr[i] = sign*step + self.arr[i]
            if self.arr[i].endswith(']],'):
                step-=1
                continue
            elif self.arr[i].endswith('],'):
                continue
            step+=1
        return self.arr

def run():
    """这个函数暂时废弃
    """
    print 'run wktformator'
            
if __name__=='__main__':

    prj = r'''PROJCS["IMAGINE GeoTIFF Support
Copyright 1991 - 2001 by ERDAS, Inc. All Rights Reserved
@(#)$RCSfile: egtf.c $ $Revision: 1.7 $ $Date: 2001/09/27 14:59:29EDT $
Projection Name = Transverse Mercator
Units = ",GEOGCS["IMAGINE GeoTIFF Support
Copyright 1991 - 2001 by ERDAS, Inc. All Rights Reserved
@(#)$RCSfile: egtf.c $ $Revision: 1.7 $ $Date: 2001/09/27 14:59:29EDT $
Unable to match Ellipsoid (Datum) to a
Geograp",DATUM["unknown",SPHEROID["unnamed",6378245,298.3000003760163]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",117],PARAMETER["scale_factor",1],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]]]'''
    fw = WktFormater(prj)
    print "\n".join(fw.format())
