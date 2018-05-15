# -*- coding: utf-8 -*-
"""该模块输出图层的元数据信息
"""

from geosings.core.Layer import *
from ReportHtmlFrame import *
from geosings.core.DataSet import DataSetType
from wktformator import WktFormater
from rliui import runUI,runApp
from geosings.core.system import SaveUtf8File, OpenUtf8
from geosings.core.system.EncodeTran import *

import base64
import os,sys

LAYER_INFO = '''
<html>
<head>
  <script type="text/javascript" src="js/ext-base.js"></script>
  <script type="text/javascript" src="js/ext-core.js"></script>
  <script type="text/javascript" src="js/ext-all.js"></script>
  <script type="text/javascript" src="js/layerinfo.js"></script>
  <script type="text/javascript" src="js/base64.js"></script>
  <link rel="stylesheet" type="text/css" href="css/ext-all.css" />
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body onload='load();'>
    <input type="hidden" id='conf' value="%s"></input>
	<div id="tabs1" align="center">
        <div id="baseinfo" class="x-hide-display" align="left">
			<div id="base"></div>
        </div>
        <div id="spatial" class="x-hide-display" align="center">
			<div id="bound" align="center"></div>
			<div id="wkt" align="left"></div>
        </div>
        <div id="attribute" class="x-hide-display" align="left">
			<div id="fields" align="left">
			</div>
        </div>
	</div>
</body>
</html>
'''

class ReportLayerInfoCtrl:
    """显示图层信息报表的控制类（非控件）
    """
    def __init__(self,layer):
        """初始化图层
        @type layer: L{geosings.core.Layer.Layer}
        @param layer: 要显示信息的图层
        """
        self.layer = layer
        self.foomap = {DataSetType.Raster:self.__GetRasterMeta,
                DataSetType.Vector:self.__GetVectorMeta}

    def Report(self):
        """显示图层信息报表
        """
        title = H2FRAME % (_('Context is as follow')+':')
        hr = HR
        name = self.layer.name
        path = self.layer.path
        geoext = self.layer.DataGeoExt
        conf = {}
        conf['title'] = _('Layer - (%s) \'s infos:') % name
        conf['name'] = name 
        conf['path'] = path 
        conf['be'] = geoext.GetRight() 
        conf['bw'] = geoext.GetLeft() 
        conf['bs'] = geoext.GetBottom() 
        conf['bn'] = geoext.GetTop() 
        if self.layer.sr == "":
            conf['wkt'] = ""
        else:
            if type(self.layer.sr) == str:
                wf = WktFormater(self.layer.sr)
            else:
                wf = WktFormater(self.layer.sr.ExportToWkt())
            conf['wkt'] = base64.encodestring('<br/>'.join(wf.format('&nbsp;'*2)))
        from geosings.tools.FieldManager import FieldLister
        lister = FieldLister(self.layer)
        fieldnames = lister.listfield()
        fields = []
        for i in range(len(fieldnames)):
            fieldrow=[i,fieldnames[i],lister.typename(i),lister.width(i),lister.precision(i)]
            fields.append(fieldrow)
        conf['fields'] = base64.encodestring(str(fields))
        #htmlstr = HTMLFRAME % (_("layer \'s infos"),
        #        _('Layer - (%s) \'s infos:') %
        #        decode2locale(self.layer.name),
        #        context) 
        context = str(conf).replace("u'", "'")
        return LAYER_INFO % context
    def __GetName(self):
        """获取图层名
        @rtype: str
        @return: 图层名
        """
        title = H2FRAME % (_('Name')+':')
        return title + decode2locale(self.layer.name)
    def __GetPath(self):
        """获取图层路径
        @rtype: str
        @return: 获取图层路径
        """
        title = H2FRAME % (_("Path")+"(URL):")
        pathstr = decode2locale(self.layer.path)
        return title+pathstr
    def __GetGeoExt(self):
        """获取图层的地理范围
        @rtype: str
        @return: 获取图层地理范围
        """
        geoext = self.layer.DataGeoExt
        title = H2FRAME % (_("Spatial Reference")+':')
        titlew = H3FRAME % (_('wkt')+':')
        titleb = H3FRAME % (_('Boundry')+':')
        westi = OLFRAME % (_("West")+" : "+str(geoext.GetLeft()))
        easti = OLFRAME % (_("East")+" : "+str(geoext.GetRight()))
        northi = OLFRAME % (_("North")+" : "+str(geoext.GetTop()))
        southi = OLFRAME % (_("South")+" : "+str(geoext.GetBottom()))
        lis = " ".join((westi,easti,northi,southi))
        if type(self.layer.sr) == str:
            wf = WktFormater(self.layer.sr)
        else:
            wf = WktFormater(self.layer.sr.ExportToWkt())
        lis2 = OLFRAME % '<br/>'.join(wf.format('&nbsp '*2))
        wktlis = titlew+lis2
        boulis = titleb+lis
        list = LISTFRAME % (boulis+wktlis)
        return title + list
    def __GetRasterMeta(self):
        """获取栅格元数据
        @rtype: str
        @return: 栅格元数据
        """
        title = H2FRAME % (_("Raster")+_("Meta")+':')
        dataset = self.layer.DataSet()
        tsize = H3FRAME % (_("Raster")+_("Size")+':')
        sizestr = '<b>'+_('Width')+':</b>' + str(dataset.RasterXSize)+ \
                '&nbsp;'*8+'<b>'+_('Height')+':</b>'+str(dataset.RasterYSize)
        sizeinfo = tsize+sizestr
        return title+sizeinfo

    def __GetVectorMeta(self):
        """获取矢量元数据
        @rtype: str
        @return: 矢量元数据
        """
        return ""

def run(*args):
    """运行整个对话框
    """
    print 'run reportlayerinfo'
    ioctrl = runUI("ReportLayerInfo")
    #print ioctrl
    if os.access( ioctrl[0], os.F_OK ):
        layer = Layer.Open(ioctrl[0])
        ctrl = ReportLayerInfoCtrl(layer)
        SaveUtf8File(ioctrl[1],ctrl.Report())

if __name__ == '__main__':
    #if len(sys.argv) == 1:#rliui废弃
    #    ioctrl = runApp()
    #    print ioctrl
    #    if os.access( ioctrl[0], os.F_OK ):
    #        layer = Layer.Open(ioctrl[0])
    #        ctrl = ReportLayerInfoCtrl(layer)
    #        SaveUtf8File(ioctrl[1],ctrl.Report())
    #else:
    #    layer = Layer.Open(sys.argv[1])
    #    ctrl = ReportLayerInfoCtrl(layer)
    #    SaveUtf8File(sys.argv[2],ctrl.Report())

    file = ("/gisdata/small_world.tif")
    layer = OpenR(file)
    ctrl = ReportLayerInfoCtrl(layer)
    print ctrl.Report()
