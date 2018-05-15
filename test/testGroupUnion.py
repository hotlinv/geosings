import ogr
from geosings.core.Layer import *
from geosings.tools.ExportFeatures import *
from geosings.tools.UnionLayer import union_layer

ds = ogr.Open("/gisdata/china",1)
layer = ds.ExecuteSQL("select * from bount_poly_gz")
ldefn = layer.GetLayerDefn()
olayer = VectorLayer(layer,ds,"")


nlayer = CreateVLayer(ds, "bount_poly_gz_union", \
    layer.GetSpatialRef(), \
    ldefn.GetGeomType(), \
    [ldefn.GetFieldDefn(i) for i in range(ldefn.GetFieldCount())])

union_layer(olayer, nlayer)
