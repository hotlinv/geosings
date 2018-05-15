#-*- encoding: utf-8 -*-
"""该模块用来执行地理相关的计算
"""

import math

kEarthRadiusKms = 6378.1370
"""地球平均半径
"""

def DistanceBetweenLocations(lat1,long1,lat2,long2):
    """这是用圆球来近似得算的，不是很精确
    @type lat1:number
    @type long1:number
    @type lat2:number
    @type long2: number
    @param lat1,long1,lat2,long2: 两个地球椭球体表面点的经纬度
    """
    dLat1InRad = lat1 * (math.pi /180.0)
    dLong1InRad = long1*(math.pi /180.0)
    dLat2InRad = lat2 * (math.pi /180.0)
    dLong2InRad = long2*(math.pi /180.0)

    dLongitude = dLong2InRad - dLong1InRad
    dLatitude = dLat2InRad - dLat1InRad

    a = math.pow(math.sin(dLatitude /2.0), 2.0)+ \
        math.cos(dLat1InRad) * math.cos(dLat2InRad) * \
        math.pow(math.sin(dLongitude /2.0), 2.0)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0-a))
    return kEarthRadiusKms * c

if __name__=="__main__":
    print DistanceBetweenLocations(22.0,33.0,23.0,33.0)
