
import ogr
from geosings.core.Layer import *
from geosings.tools.ExportFeatures import *

layerns = ["bount_poly_fj_union",
        "bount_poly_jx_union",
        "bount_poly_gx_union",
        "bount_poly_hn_union",
        "bount_poly_hain_union",
        "bount_poly_gz_union"
        ]

ds = ogr.Open("/gisdata/guangdong",1)
layer = ds.ExecuteSQL("select * from "+layerns[0])
ldefn = layer.GetLayerDefn()
olayer = VectorLayer(layer,ds,"")

nlayer = CreateVLayer(ds, "bount_poly_prov", \
    layer.GetSpatialRef(), \
    ldefn.GetGeomType(), \
    [ldefn.GetFieldDefn(i) for i in range(ldefn.GetFieldCount())])


for layern in layerns:
    layer = ds.ExecuteSQL("select * from "+layern)
    olayer = VectorLayer(layer, ds, "")
    olayer.ResetReading()
    feature = olayer.GetNextFeature()
    while feature:
        nlayer.CreateFeature(feature)
        feature = olayer.GetNextFeature()

nlayer.SyncToDisk()

