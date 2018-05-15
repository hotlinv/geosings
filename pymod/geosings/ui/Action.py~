# -*- coding: utf-8 -*-
"""
这里是管理所有ui涉及的操作动作的地方

 - writer:linux_23; create: ; version:1; 创建
 - linux_23: 2007.5.29; 添加标注命令响应
 - linux_23: 2007.9.7; 添加Select命令
"""

import os, wx

from geosings.core.Layer import *
from geosings.core.gssconst import *
from geosings.core.system.DefConf import DOCHOME
from geosings.core.system.GLog import *
from geosings.core.Annotate import AnnotateProps
from geosings.core.Exception import *

from geosings.tools.ReportAttrTable import ReportAttrTable
from geosings.tools.ReportLayerInfo import ReportLayerInfoCtrl

from geosings.ui.commondlg.OpenDlg import OpenLayerDlg

from geosings.ui.core.UIConst import *
from geosings.ui.core.Document import *
from geosings.ui.commondlg.TablePanel import *
from geosings.ui.commondlg.ReportPanel import HtmlFrame

def Open_V(path="",force=False):
    """打开一个图层的操作
    @type path: str
    @param path: 打开Layer所要用的连接字符串
    @type force: bool
    @param force: 如果有Layer已经打开且Document没有保存,是否强制打开
    @rtype: ActionResult
    @return: 返回操作的状态。
    """
    if path == "":
        dlg = OpenLayerDlg(None,'v')
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
        else:
            dlg.Destroy()
            return ActionResult.Successed
    try:
        #factory = LayerFactory()
        layer = OpenV(path)
        from geosings.ui.PyMainPanel import GetMainPanel
        GetMainPanel().canvas.map.AddLayer(layer)
    except :
        error('open file failure : %s',mainDocument.ErrNo)
        raise 
        #return ActionResult.Failuse
    return ActionResult.UpdateAll

def Open_R(path="",force=False):
    """打开一个图层的操作
    @type path: str
    @param path: 打开Layer所要用的连接字符串
    @type force: bool
    @param force: 如果有Layer已经打开且Document没有保存,是否强制打开
    @rtype: ActionResult
    @return: 返回操作的状态。
    """
    if path == "":
        dlg = OpenLayerDlg(None,'r')
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
        else:
            dlg.Destroy()
            return ActionResult.Successed
    try:
        #factory = LayerFactory()
        layer = OpenR(path)
        from geosings.ui.PyMainPanel import GetMainPanel
        GetMainPanel().canvas.map.AddLayer(layer)
    except :
        error('open file failure : %s',mainDocument.ErrNo)
        raise 
        #return ActionResult.Failuse
    return ActionResult.UpdateAll

def Close(name=None):
    """移除一个图层的操作
    @type name: str
    @param name: 要移除的图层的名称
    @rtype: ActionResult
    @return: 返回操作的状态。
    """
    try:
        from geosings.ui.PyMainPanel import GetMainPanel
        if name is None or name=="":
            GetMainPanel().canvas.map.RemoveLayer()
        else:
            GetMainPanel().canvas.map.RemoveLayer(name)
    except:
        info( 'can not close layer.%s' % name,mainDocument.ErrNo)
        raise
    return ActionResult.UpdateAll

def Top(name):
    """将一个图层置顶
    @type name: str
    @param name: 要置顶的图层名称
    @rtype: ActionResult
    @return: 返回操作的状态。
    """
    try:
        from geosings.ui.PyMainPanel import GetMainPanel
        GetMainPanel().canvas.map.TopLayer(name)
    except:
        info( 'can not top layer %s.' , name)
        raise
    return ActionResult.UpdateAll

def ZoomTo(name):
    """放大到一个图层范围
    @type name: str
    @param name: 要查看的图层名称
    @rtype: ActionResult
    @return: 返回操作的状态。
    """
    try:
        from geosings.ui.PyMainPanel import GetMainPanel
        map = GetMainPanel().canvas.map
        findn = map.GetLayerAt(name)
        if findn != -1:
            layer = map.layers[findn]
            GetMainPanel().canvas.geoext = layer.geoext
        else:
            raise LayerNoFoundErr()
    except (GssException,e):
        info( 'can not zoom to layer %s. %s' , name, e.GetMessage())
        raise 
    return ActionResult.UpdateAll

def Select(selstr):
    """选择Feature并高亮
    @type selstr: str
    @parame selstr: 选择条件
    """
    import re
    from geosings.ui.PyMainPanel import GetMainPanel
    #s = '* from aa where aaaa=11'
    restr = r'^\s*((utf8|cp936|gbk)\(){0,1}\*\){0,1}\sfrom\s(\w+)\swhere\s(.+)'
    m = re.match(restr,selstr)
    if m is None:
        info('error sql:select %s',selstr)
        raise InvalidSQLErr()
    g = m.groups()
    GetMainPanel().canvas.map.SetWhere(g[2],g[3],g[1])
    return ActionResult.UpdateAll

def __searchStr(selstr,dataset,strfields):
    where = " or ".join(["%s like '%%%s%%'" % (fname,selstr) for fname in strfields])
    debug(where)
    #oldexp = dataset.GetAttributeFilter()
    h = dataset.SetAttributeFilter(where)
    if dataset.GetFeatureCount()==0 or h!=0:
        return []
    dataset.ResetReading()
    ret = [dataset.GetNextFeature() for i in \
        range(dataset.GetFeatureCount())]
    dataset.SetAttributeFilter("")
    return ret

def Search(selstr):
    """搜索匹配的字符串
    @type selstr: str
    @parame selstr: 需要匹配的字符串
    """
    from geosings.core.system.EncodeTran import astr2sth
    from geosings.ui.PyMainPanel import GetMainPanel
    layers = GetMainPanel().canvas.map.GetSelectedLayers()
    if len(layers)==0:#如果没有选中任何图层，就全部扫描过去
        layers = GetMainPanel().canvas.map.layers
    features = {}
    for layer in layers:
        name = layer.name
        dataset = layer.DataSet()
        layerdefn = dataset.GetLayerDefn()
        fieldcount = layerdefn.GetFieldCount()
        strfields  = []
        for fi in range(fieldcount):
            fielddefn = layerdefn.GetFieldDefn(fi)
            if fielddefn.GetType()==ogr.OFTString or \
                fielddefn.GetType()==ogr.OFTWideString:
                strfields.append(fielddefn.GetName())
        if len(strfields)>0:
            fs1=__searchStr(astr2sth(selstr,"utf-8"),dataset,strfields)
            fs2=__searchStr(astr2sth(selstr,"cp936"),dataset,strfields)
            if (len(fs1)>0 or len(fs2)>0) and (name not in features):
                features[name]=[]
            if len(fs1)>0:
                features[name].extend(fs1)
            if len(fs2)>0:
                features[name].extend(fs2)
            #dataset.SetAttributeFilter(oldexp)
        info("select %d feature from layer %s",len(features[name]),name)

    from geosings.ui.PyMainPanel import GetMainPanel
    GetMainPanel().searchPanel.SetResult(features)

def Label(order):
    """标注一个图层
    @type order: str
    @param order: 要标注的图层名称，以及要标志的域名
    @rtype: ActionResult
    @return: 返回操作的状态。
    """
    ordermap = order.split()
    layname = ordermap[0]
    confstr = " ".join(ordermap[1:])
    conflist = confstr.split(";")
    confmap = {}
    for conf in conflist:
        try:
            key,val = conf.split("=")
            confmap[key] = val
        except:
            pass
    try:
        from geosings.ui.PyMainPanel import GetMainPanel
        layer = GetMainPanel().canvas.map.GetLayer(layname)
        layer.labelProps = AnnotateProps(confmap)
    except:
        info( 'can not get layer %s. ' , layname)
        raise
    return ActionResult.UpdateAll

def UnLabel(layername):
    """取消标注一个图层
    """
    try:
        from geosings.ui.PyMainPanel import GetMainPanel
        layer = GetMainPanel().canvas.map.GetLayer(layername)
        layer.labelProps = None
    except:
        info('can not get layer.%s' , layname, mainDocument.ErrNo)
        raise
    return ActionResult.UpdateAll

def ExportMap(oimgPath):
    """导出一个图层为一个图片
    """
    from geosings.ui.core.wxDC import MemDCClass
    from geosings.ui.PyMainPanel import GetMainPanel
    panel = GetMainPanel()
    canvas = panel.canvas
    rect = canvas.GetClientRect()
    dcobj = MemDCClass(rect.GetWidth(),rect.GetHeight())
    dc = dcobj.GetMemDC()
    canvas.DoDrawing(dc)
    dcobj.SaveImage(oimgPath)
    dcobj.SaveGeoInfo(mainDocument.geoext,oimgPath)

def ExportMapAll(oimgPath):
    """导出一个图层为一个图片
    """
    from geosings.ui.core.wxDC import MemDCClass
    from geosings.ui.PyMainPanel import GetMainPanel
    panel = GetMainPanel()
    canvas = panel.canvas
    geoext = mainDocument.geoext
    allgeoext = canvas.map.allGeoExt
    dcrect = canvas.GetClientRect()
    allw = allgeoext.GetWidth()/geoext.GetWidth()*dcrect.GetWidth()
    allh = allgeoext.GetHeight()/geoext.GetHeight()*dcrect.GetHeight()
    dcobj = MemDCClass(allw,allh)
    dc = dcobj.GetMemDC()
    canvas.DoDrawing(dc,all=True)
    dcobj.SaveImage(oimgPath)
    dcobj.SaveGeoInfo(allgeoext,oimgPath)

def Visible(layername):
    """使一个图层可见
    @type layername: str
    @param layername: 要可见的图层名称
    @rtype: ActionResult
    @return: 返回操作的状态
    """
    try:
        from geosings.ui.PyMainPanel import GetMainPanel
        GetMainPanel().canvas.map.VisibleLayer(layername)
    except:
        info( 'can not v layer.%s %s' % (layername, mainDocument.ErrNo))
        raise
    return ActionResult.UpdateAll

def UVisible(layername):
    """使一个图层不可见
    @type layername: str
    @param layername: 要不可见的图层名称
    @rtype: ActionResult
    @return: 返回操作的状态
    """
    try:
        from geosings.ui.PyMainPanel import GetMainPanel
        GetMainPanel().canvas.map.UVisibleLayer(layername)
    except:
        info('can not !v layer.%s %s' % (layername, mainDocument.ErrNo))
        raise
    return ActionResult.UpdateAll

def ShowHelp():
    """展示帮助文档
    @rtype: ActionResult
    @return: 返回操作的状态
    """
    os.system("\""+DOCHOME+"\\index.html\"")
    return ActionResult.Successed

def Info(layername):
    """显示图层的信息
    @type layername: str
    @param layername: 要获取和显示信息的图层名称
    @rtype: ActionResult
    @return: 返回操作的状态
    """
    try:
        from geosings.ui.PyMainPanel import GetMainPanel
        layer = GetMainPanel().canvas.map.GetLayer(layername)
        if not layer: raise LayerNoFoundErr()
        #infoframe = HtmlFrame(None,-1,"")
        #infoctrl = ReportLayerInfoCtrl(layer)
        #infoframe.LoadString(infoctrl.Report())
        #infoframe.Show()
        import webbrowser
        webbrowser.open("http://localhost:2386/LayerInfos?layer=%s&t=%s" % (layer.path,layer.type), 1)
    except:
        info('can not i layer.%s %s' % (layername, mainDocument.ErrNo))
        raise
    return ActionResult.UpdateAll

def Table(layername=None):
    """展示一个图层的属性表
    @type layername: str
    @param layername: 要获取属性表的图层名称
    @rtype: ActionResult
    @return: 返回操作的状态
    """
    try:
        from geosings.ui.PyMainPanel import GetMainPanel
        if layername is None:
            _map = GetMainPanel().canvas.map
            selection = _map.GetSelectedLayersItems()
            if len(selection)>0:
                layer = _map.GetLayer(selection[0])
            else:
                layer = _map.GetLayer(_map.GetLayerCount()-1)
        else:
            layer = GetMainPanel().canvas.map.GetLayer(layername)
        if not layer: raise LayerNoFoundErr()
        tabFrame = TableFrame(GetMainPanel())
        tabctrl = ReportAttrTable(layer)
        cols ,vals = tabctrl.GetTable()
        tabFrame.SetData(cols,vals)
        tabFrame.Show()
    except:
        info('can not tab layer:%s' % layername, mainDocument.ErrNo)
        raise
    return ActionResult.UpdateAll

def Edit(conffile=""):
    """打开一个数据的配置文件（工程文件）
    @type conffile: str
    @param conffile: 打开的配置文件（工程文件），如果为空则打开对话框
    @rtype: ActionResult
    @return: 返回操作的状态
    """
    if conffile == "":
        wildcard = "geosings prjfile (*.gsd)|*.gsd|"     \
                    "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            None, message="Open proj as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            conffile = dlg.GetPath()
            dlg.Destroy()
        else:
            error("can not Open doc")
            dlg.Destroy()
            return ActionResult.Failuse
    try:
        mainDocument.OpenDocument(conffile)
    except:
        error('can not Open doc :%s' % conffile, mainDocument.ErrNo)
        raise
    return ActionResult.UpdateAll

def Save(conffile=""):
    """保存一个数据的配置文件（工程文件）
    @type conffile: str
    @param conffile: 要把配置文件（工程文件）保存的路径
    @rtype: ActionResult
    @return: 返回操作的状态
    """
    if conffile == "":
        wildcard = "geosings prjfile (*.gsd)|*.gsd|"     \
                    "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            None, message="Save proj as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            conffile = dlg.GetPath()
            dlg.Destroy()
        else:
            error("can not save doc")
            dlg.Destroy()
            return 
    try:
        mainDocument.SaveDocument(conffile)
    except:
        error('can not save doc :%s' % conffile, mainDocument.ErrNo)
        raise
    return ActionResult.UpdateAll
    

def Exit():
    """退出系统
    """
    import sys
    sys.exit()

def SetConf(keyAndValue):
    """设置某个系统参数
    """
    from geosings.core.system.GssConfDict import GSSCONF
    keyval = keyAndValue.split("=")
    if type(keyval)!=list or len(keyval)!=2:
        error(E("invalid value"))
        return
    key,val = keyval[0],keyval[1]
    try:
        if key in GSSCONF:
            oldval = GSSCONF[key]
            if type(oldval)==str or type(oldval)==unicode:
                GSSCONF[key] = val
            else:
                try:
                    GSSCONF[key] = (type(oldval))(val)
                except Exception, arg:
                    error(E("can't convert data type")+arg)
            print GSSCONF[key]
            #return ActionResult.UpdateAll
        else:
            error(E("Can't find this key"),key)
    except Exception, arg:
        error(arg)

#def OnMenuMode(event):
#    """菜单或者工具栏选择了一个模式
#    """
#    id = event.GetId()
#    mainPanel = PyMainPanel.GetMainPanel()
#    if id == ID_MB_NoMode or id == ID_TB_NoMode:
#        mode = ModeKey.NoneMode
#    elif id == ID_MB_Pan or id == ID_TB_Pan:
#        mode = ModeKey.PanMode
#    elif id==ID_MB_ZoomIn or id==ID_TB_ZoomIn:
#        mode = ModeKey.ZoomInMode
#    elif id==ID_MB_ZoomOut or  id==ID_TB_ZoomOut:
#        mode = ModeKey.ZoomOutMode
#    elif id==ID_MB_Info or  id==ID_TB_Info:
#        mode = ModeKey.InfoMode
#    mainPanel.SetMode( mode)

#def OnMenuMsg(event):
#    """菜单或者工具栏选择了一个命令
#    """
#    id = event.GetId()
#    mainPanel = PyMainPanel.GetMainPanel()
#    if id == ID_MB_Open or id == ID_TB_Open:
#        result = Edit()
#    elif id == ID_MB_Save or id == ID_TB_Save:
#        result = Save()
#    elif id == ID_MB_AddLayer or id == ID_TB_AddLayer:
#        result = Open()
#    elif id == ID_MB_Exit:
#        result = Exit()
#    if result == ActionResult.UpdateAll:
#        from PyMainPanel import GetMainPanel
#        mainpanel = GetMainPanel()
#        mainpanel.ReDrawCanvas()
#        mainpanel.UpdateDataList()
