# -*- coding: utf-8 -*-
"""绘制样式配置类
"""

import wx, ogr, copy, os
from geosings.core.Symbol import *
from geosings.ui.core.wxSymbol import *
import geosings.core.system.UseGetText
import  wx.lib.colourselect as  csel
from geosings.ui.core.MainImage import GetStyleDirPath

class SymbolPanel(wx.Panel):
    """绘制Symbol例子的面板
    """
    def __init__(self,parent, symbol,*args,**kwds):
        wx.Panel.__init__(self,parent,*args,**kwds)
        self.symbol = symbol
        self.parent = parent
        self.symc_evt = None
        self.Bind(wx.EVT_PAINT, self.OnSymPaint)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDClick)

    def OnDClick(self,evt):
        #print 'click'
        tmp = copy.deepcopy(self.symbol)
        dlg = SymbolSelectDialog(self, tmp, -1)
        r = dlg.ShowModal()
        if r == wx.ID_OK:
            self.symbol.clear()
            for k in tmp.keys():
                self.symbol[k] = tmp[k]
        self.parent.Refresh()
        if self.symc_evt is not None:
            self.symc_evt()
    def RegSymbolChanged(self, evt):
        self.symc_evt = evt
    
    def OnSymPaint(self, evt):
        """需要重绘时响应的事件
        @type evt: wxEvent
        @param evt: wxEVT_PAINT事件
        """
        self.__DrawSymbol()
    
    def __DrawSymbol(self):
        """绘制图层的图例
        """
        symbol = self.symbol
        type = symbol['type']
        dc = wx.PaintDC(self) 
        dc.Clear()
        self.PrepareDC(dc)
        dc.BeginDrawing()
        size = self.GetSize()
        width = size.GetWidth()
        height = size.GetHeight()
        w = width; h = height
        centerp = (width/2,height/2)
        l,t,w,h = centerp[0]-w/2,centerp[1]-h/2,w,h
        if symbol['type']==SymbolType.POINT:
            peno = dc.GetPen()
            pen = getPanSymbol(symbol)
            brusho = dc.GetBrush()
            brush = getBrushSymbol(symbol)
            symsize = getSizeSymbol(symbol)
            dc.SetPen(pen)
            dc.SetBrush(brush)
            dc.DrawCirclePoint(centerp,symsize)
            dc.SetPen(peno)
            dc.SetBrush(brusho)
        elif symbol['type']==SymbolType.LINE:
            peno = dc.GetPen()
            pen = getPanSymbol(symbol)
            dc.SetPen(pen)
            dc.DrawLines([(l,t),(l+w,t+h)],0,0)
            dc.SetPen(peno)
        elif symbol['type'] == SymbolType.POLYGON:
            peno = dc.GetPen()
            pen = getPanSymbol(symbol)
            brusho = dc.GetBrush()
            brush = getBrushSymbol(symbol)
            dc.SetPen(pen)
            dc.SetBrush(brush)
            dc.DrawRectangle(l,t,w,h)
            dc.SetPen(peno)
            dc.SetBrush(brusho)
        elif symbol['type'] == 'raster':
            from geosings.ui.core.MainImage import GetRasterSymbol
            bmp = GetRasterSymbol()
            dc.DrawBitmap(bmp,l,t,True)
            pass
        dc.EndDrawing()

class SimplePointSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.symbol = symbol
        #self.colorbut = wx.Button(self, -1, "")
        self.colorbut = csel.ColourSelect(self, -1, "", symbol["color"],
                size = (30,20))
        self.sizesc = wx.SpinCtrl(self, -1, "")
        self.sizesc.SetRange(1,100)
        self.sizesc.SetValue(symbol["size"])
        self.colorbut.Bind(csel.EVT_COLOURSELECT, parent.ChangeColor)
        self.sizesc.Bind(wx.EVT_SPINCTRL, parent.ChangeSize)
        

        box = wx.StaticBox(self, -1, _("Option"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.FlexGridSizer(cols=2, vgap=4, hgap=4)
        sizer_2.Add(wx.StaticText(self,-1,_("color")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.colorbut, 0, wx.ADJUST_MINSIZE, 10)
        sizer_2.Add(wx.StaticText(self,-1,_("size")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.sizesc, 0, wx.ADJUST_MINSIZE, 10)
        bsizer.Add(sizer_2, 1, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(bsizer, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

class PointSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.symbol = symbol
        self.parent = parent
        self.cbmap = {_("Simple Point"):SimplePointSymbolSelectPanel}
        cblist = self.cbmap.keys()
        self.cb = wx.ComboBox(self, 500, cblist[0] , (90, 50), 
            (95, -1), cblist, wx.CB_DROPDOWN|wx.CB_READONLY )
        self.__SelectPanel(cblist[0])

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.cb, 0, wx.EXPAND|wx.ALL, 10)
        sizer_1.Add(self.confpanel, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()
    def __SelectPanel(self, key):
        if getattr(self, "confpanel", None) is not None:
            self.confpanel.Destroy()
        self.confpanel = self.cbmap[key](self, self.symbol, -1)
    def OnSelectPanel(self, evt):
        key = evt.GetValue()
        self.__SelectPanel(key)
    def ChangeColor(self, evt):
        color = evt.GetValue()
        self.symbol["color"] = color
        self.parent.RefreshPreview()
    def ChangeSize(self, evt):
        #size = evt.GetPosition()
        size = evt.GetInt()
        self.symbol["size"] = size
        self.parent.RefreshPreview()

class SimpleLineSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.symbol = symbol
        self.parent = parent
        #self.colorbut = wx.Button(self, -1, "")
        self.cbmap = {_("DOT"):wx.DOT ,
                _("LONG_DASH"):wx.LONG_DASH ,
                _("SHORT_DASH"):wx.SHORT_DASH ,
                _("DOT_DASH"):wx.DOT_DASH ,
                _("USER_DASH"):wx.USER_DASH ,
                _("BDIAGONAL_HATCH"):wx.BDIAGONAL_HATCH ,
                _("CROSSDIAG_HATCH"):wx.CROSSDIAG_HATCH ,
                _("FDIAGONAL_HATCH"):wx.FDIAGONAL_HATCH ,
                _("CROSS_HATCH"):wx.CROSS_HATCH ,
                _("HORIZONTAL_HATCH"):wx.HORIZONTAL_HATCH ,
                _("VERTICAL_HATCH"):wx.VERTICAL_HATCH
        }
        cblist = self.cbmap.keys()
        self.cb = wx.ComboBox(self, 500, cblist[0] , (90, 50), 
            (95, -1), cblist, wx.CB_DROPDOWN|wx.CB_READONLY )

        self.colorbut = csel.ColourSelect(self, -1, "", symbol["color"],
                size = (30,20))
        self.sizesc = wx.SpinCtrl(self, -1, "")
        self.sizesc.SetRange(1,100)
        self.sizesc.SetValue(symbol["size"])
        self.colorbut.Bind(csel.EVT_COLOURSELECT, parent.ChangeColor)
        self.sizesc.Bind(wx.EVT_SPINCTRL, parent.ChangeSize)
        self.cb.Bind(wx.EVT_COMBOBOX, self.SelectHatch)
        

        box = wx.StaticBox(self, -1, _("Option"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.FlexGridSizer(cols=2, vgap=4, hgap=4)
        sizer_2.Add(wx.StaticText(self,-1,_("color")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.colorbut, 0, wx.ADJUST_MINSIZE, 10)
        sizer_2.Add(wx.StaticText(self,-1,_("Style")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.cb)
        sizer_2.Add(wx.StaticText(self,-1,_("size")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.sizesc, 0, wx.ADJUST_MINSIZE, 10)
        bsizer.Add(sizer_2, 1, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(bsizer, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

    def SelectHatch(self,evt):
        styname = self.cb.GetValue()
        self.parent.symbol["hatch"] = self.cbmap[styname]
        self.parent.parent.RefreshPreview()

class LineSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.symbol = symbol
        self.parent = parent
        self.cbmap = {_("Simple Line"):SimpleLineSymbolSelectPanel}
        cblist = self.cbmap.keys()
        self.cb = wx.ComboBox(self, 500, cblist[0] , (90, 50), 
            (95, -1), cblist, wx.CB_DROPDOWN|wx.CB_READONLY )
        self.__SelectPanel(cblist[0])

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.cb, 0, wx.EXPAND|wx.ALL, 10)
        sizer_1.Add(self.confpanel, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()
    def __SelectPanel(self, key):
        if getattr(self, "confpanel", None) is not None:
            self.confpanel.Destroy()
        self.confpanel = self.cbmap[key](self, self.symbol, -1)
    def OnSelectPanel(self, evt):
        key = evt.GetValue()
        self.__SelectPanel(key)
    def ChangeColor(self, evt):
        color = evt.GetValue()
        self.symbol["color"] = color
        self.parent.RefreshPreview()
    def ChangeSize(self, evt):
        #size = evt.GetPosition()
        size = evt.GetInt()
        self.symbol["size"] = size
        self.parent.RefreshPreview()

class NoFillSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.symbol = symbol
        self.parent = parent
        symbol['color']=None
        self.sizesc = wx.SpinCtrl(self, -1, "")
        self.sizesc.SetRange(1,100)
        self.sizesc.SetValue(symbol["size"])
        self.olcolorbut = csel.ColourSelect(self, -1, "", symbol["olcolor"],
                size = (30,20))
        self.olcolorbut.Bind(csel.EVT_COLOURSELECT, parent.ChangeOLColor)
        self.sizesc.Bind(wx.EVT_SPINCTRL, parent.ChangeSize)
        

        box = wx.StaticBox(self, -1, _("Option"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.FlexGridSizer(cols=2, vgap=4, hgap=4)
        sizer_2.Add(wx.StaticText(self,-1,_("size")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.sizesc, 0, wx.ADJUST_MINSIZE, 10)
        sizer_2.Add(wx.StaticText(self,-1,_("outline color")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.olcolorbut, 0, wx.ADJUST_MINSIZE, 10)
        bsizer.Add(sizer_2, 1, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(bsizer, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

        #加载初始配置   
        if 'bitmap' in self.parent.symbol:
            self.parent.symbol.pop('bitmap')
        if 'hatch' in self.parent.symbol:
            self.parent.symbol.pop('hatch')
        self.parent.RefreshPreview()


class SimpleFillSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.symbol = symbol
        self.parent = parent
        #self.colorbut = wx.Button(self, -1, "")
        self.colorbut = csel.ColourSelect(self, -1, "", symbol["color"],
                size = (30,20))
        self.sizesc = wx.SpinCtrl(self, -1, "")
        self.sizesc.SetRange(1,100)
        self.sizesc.SetValue(symbol["size"])
        self.olcolorbut = csel.ColourSelect(self, -1, "", symbol["olcolor"],
                size = (30,20))
        self.colorbut.Bind(csel.EVT_COLOURSELECT, parent.ChangeColor)
        self.olcolorbut.Bind(csel.EVT_COLOURSELECT, parent.ChangeOLColor)
        self.sizesc.Bind(wx.EVT_SPINCTRL, parent.ChangeSize)
        

        box = wx.StaticBox(self, -1, _("Option"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.FlexGridSizer(cols=2, vgap=4, hgap=4)
        sizer_2.Add(wx.StaticText(self,-1,_("color")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.colorbut, 0, wx.ADJUST_MINSIZE, 10)
        sizer_2.Add(wx.StaticText(self,-1,_("size")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.sizesc, 0, wx.ADJUST_MINSIZE, 10)
        sizer_2.Add(wx.StaticText(self,-1,_("outline color")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.olcolorbut, 0, wx.ADJUST_MINSIZE, 10)
        bsizer.Add(sizer_2, 1, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(bsizer, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

        #加载初始配置   
        if 'bitmap' in self.parent.symbol:
            self.parent.symbol.pop('bitmap')
        if 'hatch' in self.parent.symbol:
            self.parent.symbol.pop('hatch')
        self.parent.RefreshPreview()


class HatchFillSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.symbol = symbol
        self.parent = parent
        self.cbmap = {_("Backward diagonal"):wx.BDIAGONAL_HATCH ,
                _("Cross-diagonal"):wx.CROSSDIAG_HATCH ,
                _("Forward diagonal"):wx.FDIAGONAL_HATCH ,
                _("Cross"):wx.CROSS_HATCH ,
                _("Horizontal"):wx.HORIZONTAL_HATCH ,
                _("Vertical"):wx.VERTICAL_HATCH }
        cblist = self.cbmap.keys()
        self.colorbut = csel.ColourSelect(self, -1, "", symbol["color"],
                size = (30,20))
        self.cb = wx.ComboBox(self, 500, cblist[0] , (90, 50), 
            (95, -1), cblist, wx.CB_DROPDOWN|wx.CB_READONLY )
        self.cb.Bind(wx.EVT_COMBOBOX, self.SelectHatch)
        self.olcolorbut = csel.ColourSelect(self, -1, "", symbol["olcolor"],
                size = (30,20))
        self.sizesc = wx.SpinCtrl(self, -1, "")
        self.sizesc.SetRange(1,100)
        self.sizesc.SetValue(symbol["size"])
        self.colorbut.Bind(csel.EVT_COLOURSELECT, parent.ChangeColor)
        self.olcolorbut.Bind(csel.EVT_COLOURSELECT, parent.ChangeOLColor)
        self.sizesc.Bind(wx.EVT_SPINCTRL, parent.ChangeSize)

        box = wx.StaticBox(self, -1, _("Option"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.FlexGridSizer(cols=2, vgap=4, hgap=4)
        sizer_2.Add(wx.StaticText(self,-1,_("Style")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.cb)
        sizer_2.Add(wx.StaticText(self,-1,_("color")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.colorbut, 0, wx.ADJUST_MINSIZE, 10)
        sizer_2.Add(wx.StaticText(self,-1,_("size")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.sizesc, 0, wx.ADJUST_MINSIZE, 10)
        sizer_2.Add(wx.StaticText(self,-1,_("outline color")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.olcolorbut, 0, wx.ADJUST_MINSIZE, 10)
        bsizer.Add(sizer_2, 1, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(bsizer, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

        #加载初始配置   
        self.SelectHatch(None)
        if 'bitmap' in self.parent.symbol:
            self.parent.symbol.pop('bitmap')

    def SelectHatch(self,evt):
        styname = self.cb.GetValue()
        self.parent.symbol["hatch"] = self.cbmap[styname]
        self.parent.RefreshPreview()

class StippleFillSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.symbol = symbol
        self.parent = parent
        styledir = GetStyleDirPath()
        stylist = os.listdir(styledir)
        stylist = [s for s in stylist if \
                os.path.isfile(os.path.join(styledir,s))]
        self.cb = wx.ComboBox(self, 500, stylist[0] , (90, 50), 
            (95, -1), stylist, wx.CB_DROPDOWN|wx.CB_READONLY )
        self.cb.Bind(wx.EVT_COMBOBOX, self.SelectBitmap)

        box = wx.StaticBox(self, -1, _("Option"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.FlexGridSizer(cols=2, vgap=4, hgap=4)
        sizer_2.Add(wx.StaticText(self,-1,_("Image")+":"), 0,
                wx.ADJUST_MINSIZE|wx.ALL, 10)
        sizer_2.Add(self.cb)
        bsizer.Add(sizer_2, 1, wx.ADJUST_MINSIZE, 0)
        sizer_1.Add(bsizer, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

        #加载初始配置   
        self.SelectBitmap(None)
        if 'hatch' in self.parent.symbol:
            self.parent.symbol.pop('hatch')

    def SelectBitmap(self,evt):
        imgname = self.cb.GetValue()
        self.parent.symbol["bitmap"] = imgname
        self.parent.RefreshPreview()

class FillSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.symbol = symbol
        self.parent = parent
        self.mainsizer = sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.cbmap = {
                _('No Fill'):NoFillSymbolSelectPanel,
                _("Simple Fill"):SimpleFillSymbolSelectPanel,
                _("Hatch Fill"):HatchFillSymbolSelectPanel,
                _("Stipple Fill"):StippleFillSymbolSelectPanel}
        cblist = self.cbmap.keys()
        self.cb = wx.ComboBox(self, 500, cblist[0] , (90, 50), 
            (95, -1), cblist, wx.CB_DROPDOWN|wx.CB_READONLY )

        self.__SelectPanel(cblist[0])
        self.Bind(wx.EVT_COMBOBOX,self.SelectPanel)

        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()

    def SelectPanel(self, evt):
        self.__SelectPanel(self.cb.GetValue())

    def __SelectPanel(self, key):
        if getattr(self, "confpanel", None) is not None:
            self.mainsizer.Clear()
            self.confpanel.Destroy()
        self.confpanel = self.cbmap[key](self, self.symbol, -1)
        self.mainsizer.Add(self.cb, 0, wx.EXPAND|wx.ALL, 10)
        self.mainsizer.Add(self.confpanel, 1, wx.EXPAND, 0)
        self.Layout()
        
    def OnSelectPanel(self, evt):
        key = evt.GetValue()
        self.__SelectPanel(key)
    def RefreshPreview(self):
        self.parent.RefreshPreview()
    def ChangeColor(self, evt):
        color = evt.GetValue()
        self.symbol["color"] = color
        self.RefreshPreview()
    def ChangeOLColor(self, evt):
        color = evt.GetValue()
        self.symbol["olcolor"] = color
        self.RefreshPreview()
    def ChangeSize(self, evt):
        #size = evt.GetPosition()
        size = evt.GetInt()
        self.symbol["size"] = size
        self.RefreshPreview()

class UnknownSymbolSelectPanel(wx.Panel):
    def __init__(self, parent, symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)

def getSymbolSelectPanel(symbol):
    symbolType = symbol["type"]
    if symbolType == ogr.wkbPoint or \
        symbolType == ogr.wkbMultiPoint:
        return PointSymbolSelectPanel
    elif symbolType == ogr.wkbLineString or \
        symbolType == ogr.wkbMultiLineString:
        return LineSymbolSelectPanel
    elif symbolType == ogr.wkbPolygon or \
        symbolType == ogr.wkbMultiPolygon:
        return FillSymbolSelectPanel
    else:
        return UnknownSymbolSelectPanel


class SymbolSelectPanel(wx.Panel):
    def __init__(self, parent,symbol, *args, **kwds):
        wx.Panel.__init__(self, parent, *args, **kwds)
        self.pv_panel = SymbolPanel(self, symbol, -1)
        self.set_panel = getSymbolSelectPanel(symbol)(self, symbol, -1)

        box = wx.StaticBox(self, -1, _("Preview"))
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        bsizer.Add(self.pv_panel, 1, wx.EXPAND|wx.ALL, 30)
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(bsizer, 1, wx.EXPAND|wx.ALL, 10)
        sizer_1.Add(self.set_panel, 1, wx.EXPAND|wx.ALL, 10)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()
    def RefreshPreview(self):
        self.pv_panel.Refresh()
        

class SymbolSelectDialog(wx.Dialog):
    def __init__(self,parent, symbol, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self,parent, *args, **kwds)
        self.panel_1 = SymbolSelectPanel(self, symbol, -1)
        self.static_line_1 = wx.StaticLine(self, -1)
        self.panel_2 = wx.Panel(self, -1)
        self.okbut = wx.Button(self, wx.ID_OK, _("OK"))
        self.canbut = wx.Button(self, wx.ID_CANCEL, _("Cancel"))

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle(_("Symbol Selector"))

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        sizer_1.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_1.Add(self.panel_2, 0, wx.EXPAND, 0)
        sizer_2.Add((1,1), 1, wx.EXPAND, 0)
        sizer_2.Add(self.okbut, 0, wx.ALL|wx.ADJUST_MINSIZE, 3)
        sizer_2.Add(self.canbut, 0, wx.ALL|wx.ADJUST_MINSIZE, 3)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 3)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()
        self.SetSize((550,400))


if __name__=="__main__":
    from geosings.ui.commondlg import TestFrame
    import ogr
#    TestFrame.RunDlgTest(SymbolSelectDialog, CreateSymbol(ogr.wkbPoint), -1)
    TestFrame.RunDlgTest(SymbolSelectDialog, CreateSymbol(ogr.wkbLineString), -1)
#    TestFrame.RunDlgTest(SymbolSelectDialog, CreateSymbol(ogr.wkbPolygon), -1)
    
