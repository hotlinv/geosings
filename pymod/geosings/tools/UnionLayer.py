# -*- encoding: utf-8 -*-
"""定义合并所有Layer的Geometry的方法

 - writer:linux_23; create: 2008.5.22; version:1; 创建
"""

def union_layer(ilayer, olayer):
    ilayer.ResetReading()

    features = [ilayer.GetNextFeature() for f in range(ilayer.GetFeatureCount())]
    gs = [f.GetGeometryRef() for f in features]

    f = features[0]

    i = 0
    g = gs.pop(0)
    gt = gs.pop(0)
    last = len(gs)
    count = last
    while len(gs):
        if len(gs)!=last:
            print '\r',count-last,'/',count,
            last = len(gs)
        if gt.Touches(g):
            g = g.Union(gt)
            gt = gs.pop(0)
            i = 0
        else:
            if i==len(gs): # loop all gs, no found
                f.SetGeometry(g)
                olayer.CreateFeature(f)
                g = gs.pop(0)
                i = 0
            else:
                gs.append(gt)
                gt = gs.pop(0)
                i+=1
    f.SetGeometry(g)
    olayer.CreateFeature(f)
    print '\r','ok!'
    olayer.SyncToDisk()


