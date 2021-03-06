import ogr
from geosings.core.Layer import *
from geosings.tools.ExportFeatures import *

def foo(f):
    a = f.GetFieldAsString("ADCODE93")
    if a.endswith('00'):
        return True
    else:
        return False

ds = ogr.Open("/gisdata/guangdong/city",1)
layer = ds.ExecuteSQL("select * from 440000_XianCh_point_44")
ldefn = layer.GetLayerDefn()
olayer = VectorLayer(layer,ds,"")

nlayer = CreateVLayer(ds, "guangdong2Copy", \
    layer.GetSpatialRef(), \
    ldefn.GetGeomType(), \
    [ldefn.GetFieldDefn(i) for i in range(ldefn.GetFieldCount())])

olayer.ResetReading()
VOgrLayerSelectionExportor(olayer).filter_output(VectorLayer(nlayer,ds,""),
        foo)
