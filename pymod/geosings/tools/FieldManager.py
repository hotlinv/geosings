# -*- coding: utf-8 -*-
"""
该模块定义字段管理工具

 - writer:linux_23; create:2008.5.7; version:1; 创建
"""
import ogr
from geosings.core.Layer import *

class FieldLister:
    def __init__(self, layer):
        self.layer = layer
        try:
            self.defn = self.layer.GetLayerDefn()
        except:
            self.defn = None
        self._make_type_dict()
        #print dir(self.defn)
    def _make_type_dict(self):
        self.__typedict = {}
        ts = [i for i in dir(ogr) if i.startswith('OFT')]
        for t in ts:
            self.__typedict[getattr(ogr,t)] = t
    def field(self, fieldi):
        if type(fieldi) == int:
            return self.defn.GetFieldDefn(fieldi)
        else:
            i = self.defn.GetFieldIndex(fieldi)
            return self.defn.GetFieldDefn(i)
    def fieldi(self, fieldi):
        if type(fieldi) == int:
            return fieldi
        else:
            return self.defn.GetFieldIndex(fieldi)
    def listfield(self):
        """列出所有的列名
        """
        if not self.defn:
            return []
        return [self.defn.GetFieldDefn(i).GetName() \
                for i in range(self.defn.GetFieldCount())]
    def type(self, fieldi):
        """数据类型
        """
        return self.field(fieldi).GetType()
    def typename(self, fieldi):
        """数据类型名
        """
        return self.__typedict[self.type(fieldi)]
    def width(self, fieldi):
        """数据宽度
        """
        return self.field(fieldi).GetWidth()
    def precision(self, fieldi):
        """数据精度
        """
        return self.field(fieldi).GetPrecision()
    def justify(self, fieldi):
        """是否对其
        """
        return self.field(fieldi).GetJustify()
class FieldManager:
    def __init__(self, datasource, layername):
        self.datasource = datasource
        self.layername = layername
        #self.ds = OpenVSource(datasource,1)
        self.layer = GetLayer(datasource, layername, 1)
        self.ds = self.layer.dataSource
        self.defn = self.layer.GetLayerDefn()
        self.lister = FieldLister(self.layer)

    def listfield(self):
        """列出所有的列名
        """
        return self.lister.listfield()
    def type(self, fieldi):
        """数据类型
        """
        return self.lister.type(fieldi)
    def typename(self, fieldi):
        """数据类型名
        """
        return self.lister.typename(fieldi)
    def width(self, fieldi):
        """数据宽度
        """
        return self.lister.width(fieldi)
    def precision(self, fieldi):
        """数据精度
        """
        return self.lister.precision(fieldi)
    def justify(self, fieldi):
        """是否对其
        """
        return self.lister.justify(fieldi)
    def field(self, fieldi):
        return self.lister.field(fieldi)
    def rename(self, fieldi, name):
        """重命名(因为ogr API的限制，只能新建图层)
        """
        field = self.field(fieldi)
        field.SetName(name)
        fields = [self.defn.GetFieldDefn(i) \
                for i in range(self.defn.GetFieldCount())]
        nlayer = CreateVLayer(self.ds, self.layer.GetName()+"_rfd", \
                self.layer.GetSpatialRef(), self.defn.GetGeomType(), fields)

        feature = self.layer.DataSet().GetNextFeature()
        while feature is not None:
            nlayer.CreateFeature(feature)
            feature = self.layer.DataSet().GetNextFeature()
        nlayer.SyncToDisk()
        return _FieldManager().set(self.ds, nlayer)
    def add(self, field):
        """添加(因为ogr API的限制，只能新建图层)
        """
        fields = [self.defn.GetFieldDefn(i) \
                for i in range(self.defn.GetFieldCount())]
        fields.append(field)
        nlayer = CreateVLayer(self.ds, self.layer.GetName()+"_afd", \
                self.layer.GetSpatialRef(), self.defn.GetGeomType(), fields)

        feature = self.layer.DataSet().GetNextFeature()
        while feature is not None:
            nlayer.CreateFeature(feature)
            feature = self.layer.DataSet().GetNextFeature()
        nlayer.SyncToDisk()
        return _FieldManager().set(self.ds, nlayer)
    def delete(self, fieldi):
        """删除(因为ogr API的限制，只能新建图层)
        """
        field = self.fieldi(fieldi)
        fields = [self.defn.GetFieldDefn(i) \
                for i in range(self.defn.GetFieldCount()) if i!=field]
        nlayer = CreateVLayer(self.ds, self.layer.GetName()+"_dfd", \
                self.layer.GetSpatialRef(), self.defn.GetGeomType(), fields)

        feature = self.layer.DataSet().GetNextFeature()
        while feature is not None:
            nlayer.CreateFeature(feature)
            feature = self.layer.DataSet().GetNextFeature()
        nlayer.SyncToDisk()
        return _FieldManager().set(self.ds, nlayer)

class _FieldManager(FieldManager):
    def __init__(self):
        pass
    def set(self, datasource, layer):
        self.datasource = datasource.GetName()
        self.layername = layer.GetName()
        self.ds = datasource
        self.layer = layer
        self.defn = self.layer.GetLayerDefn()
        self.lister = FieldLister(self.layer)
        return self

if __name__=="__main__":
    fm = FieldManager("g:/gisdata/fujian", "region")
    fields = fm.listfield()
    print " "*10, " | ".join(fm.listfield())

    for field in range(len(fields)):
        print fm.typename(field), fm.width(field), \
                fm.precision(field), fm.justify(field)

    #fm.rename(fields[0],"AAA")
    #fm2 = fm.delete('NAME')

    #print " "*10, " | ".join(fm2.listfield())


    fm3 = fm.rename("name",'name2')
    print " "*10, " | ".join(fm3.listfield())
