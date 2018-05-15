# -*- coding: utf-8 -*-
"""
管理UI的配置。包括读取用户配置。

 - writer:linux_23; create: ; version:1; 创建
 - linux_23: 把MsgKeyWord的键设置移到这里
"""

import Action  
import os,wx

from geosings.core.system.GssConfDict import GSSCONF
from geosings.core.system.RunSysConf import RunSysConf

from geosings.ui.core.UIConst import *
from MsgKeyWord import ReInitMsgWordMap 


GSSCONF["CANV_OP_MSG_NUM"] = 6
GSSCONF["SHOW_COORD"] = 'O'#设置G可以显示相应地理坐标
GSSCONF["HAS_MODE_LABEL"] = 0
GSSCONF["HAS_TOOLBAR_TEXT"] = True
GSSCONF["TOOLBAR_BITMAP_WIDTH"] = 22
GSSCONF["TOOLBAR_BITMAP_HEIGHT"] = 22
GSSCONF["TOOLBAR_BITMAP_SIZE"] = wx.Size(GSSCONF["TOOLBAR_BITMAP_WIDTH"],
        GSSCONF["TOOLBAR_BITMAP_HEIGHT"])

GSSCONF["HAS_MODE_LABEL"] = True
GSSCONF["CANV_BACKGROUND_COLOR"] = "#aaffdd"

GSSCONF["HL_COLOR"] = "#ffff00"#高亮选择颜色

GSSCONF["ERR_COLOR"] = "#ff0000"#错误信息颜色
GSSCONF["INFO_COLOR"] = "#00ff00"#普通信息颜色
GSSCONF["LOG_COLOR"] = "#0000ff"#LOG信息颜色
GSSCONF["DEBUG_COLOR"] = "#777777"#调试信息颜色

GSSCONF["OPEN_H_STR"] = "Open a prj file"
GSSCONF["SAVE_H_STR"] = "Save a prj file"
GSSCONF["TABLE_H_STR"] = "Show DataSet Attribute Table"
GSSCONF["EXIT_H_STR"] = "Exit the application"
GSSCONF["NOMODE_H_STR"] = "no mode"
GSSCONF["PANMODE_H_STR"] = "pan mode"
GSSCONF["ZOOMIN_H_STR"] = "zoomin mode"
GSSCONF["ZOOMOUT_H_STR"] = "zoomout mode"
GSSCONF["INFO_H_STR"] = "info mode"
GSSCONF["ADD_VLAYER_H_STR"] = "Add a Vector Layer"
GSSCONF["ADD_RLAYER_H_STR"] = "Add a Raster Layer"
GSSCONF["REMOVE_LAYER_H_STR"] = "Remove a layer"
GSSCONF["FULL_H_STR"] = "Show the full layer"
GSSCONF["RM_LAYER_H_STR"] = "Remove Selected Layer(s)"

GSSCONF['HANDLER_CONF'] = {}

mwm = ReInitMsgWordMap()#初始化消息列表
mwm.SetKeyMap("MSG_KEY_OPENV", ":ov", Action.Open_V)
mwm.SetKeyMap("MSG_KEY_OPENR", ":or", Action.Open_R)
mwm.SetKeyMap("MSG_KEY_EXIT", ":q", Action.Exit)
mwm.SetKeyMap("MSG_KEY_CLOSE", ":r", Action.Close)
mwm.SetKeyMap("MSG_KEY_TOP", ":top", Action.Top)
mwm.SetKeyMap("MSG_KEY_VISIBLE", ":v", Action.Visible)
mwm.SetKeyMap("MSG_KEY_UVISIBLE", ":v!", Action.UVisible)
mwm.SetKeyMap("MSG_KEY_HELP", ":h", Action.ShowHelp)
mwm.SetKeyMap("MSG_KEY_INFO", ":i", Action.Info)
mwm.SetKeyMap("MSG_KEY_TABLE", ":tab", Action.Table)
mwm.SetKeyMap("MSG_KEY_EDIT", ":e", Action.Edit)
mwm.SetKeyMap("MSG_KEY_SELECT", ":select", Action.Select)
mwm.SetKeyMap("MSG_KEY_SEARCH", ":search", Action.Search)
mwm.SetKeyMap("MSG_KEY_SAVE", ":save", Action.Save)
mwm.SetKeyMap("MSG_KEY_LABEL", ":lab", Action.Label)
mwm.SetKeyMap("MSG_KEY_ULABEL", ":lab!", Action.UnLabel)
mwm.SetKeyMap("MSG_KEY_EXPORTMAP", ":exp", Action.ExportMap)
mwm.SetKeyMap("MSG_KEY_EXPORTMAP_ALL", ":expall", Action.ExportMapAll)
mwm.SetKeyMap("MSG_KEY_SET", ":set", Action.SetConf)
mwm.SetKeyMap("MSG_KEY_ZOOM_TO_LAYER", ":zt", Action.ZoomTo)
mwm.SetKeyMap("MSG_KEY_FULL", "f")
mwm.SetKeyMap("MSG_KEY_DRAW", "d")
mwm.SetKeyMap("MSG_KEY_MODE_NO", "n")
mwm.SetKeyMap("MSG_KEY_MODE_PAN", 't')
mwm.SetKeyMap("MSG_KEY_MODE_ZOOMIN", "Z")
mwm.SetKeyMap("MSG_KEY_MODE_ZOOMOUT", "z")
mwm.SetKeyMap("MSG_KEY_MODE_INFO", "q")
mwm.SetKeyMap("MSG_KEY_LEFT", 'h')
mwm.SetKeyMap("MSG_KEY_RIGHT", 'l')
mwm.SetKeyMap("MSG_KEY_DOWN", 'j')
mwm.SetKeyMap("MSG_KEY_UP", 'k')
mwm.SetKeyMap("MSG_KEY_AIM", 'a')

from geosings.ui.gmap.GOperHandler import PanHandler, ZoomInHandler,ZoomOutHandler, NoModeHandler
GSSCONF['HANDLER_CONF'][ModeKey.NoneMode] = NoModeHandler
GSSCONF['HANDLER_CONF'][ModeKey.PanMode] = PanHandler
GSSCONF['HANDLER_CONF'][ModeKey.ZoomInMode] = ZoomInHandler
GSSCONF['HANDLER_CONF'][ModeKey.ZoomOutMode] = ZoomOutHandler

EDIT_MSG = 'MSG_KEY_EDIT'
EXIT_MSG = 'MSG_KEY_EXIT'
OPENV_MSG = 'MSG_KEY_OPENV'
OPENR_MSG = 'MSG_KEY_OPENR'
SAVE_MSG = 'MSG_KEY_SAVE'
TABLE_MSG = 'MSG_KEY_TABLE'
CLOSE_MSG = 'MSG_KEY_CLOSE'

FULL_MSG = 'MSG_KEY_FULL'
NOMODE_MSG = 'MSG_KEY_MODE_NO'
PANMODE_MSG = 'MSG_KEY_MODE_PAN'
ZOOMINMODE_MSG = 'MSG_KEY_MODE_ZOOMIN'
ZOOMOUTMODE_MSG = 'MSG_KEY_MODE_ZOOMOUT'
INFOMODE_MSG = 'MSG_KEY_MODE_INFO'

tmptoolbarconf = []
GSSCONF["TOOLBAR_CONF"] = tmptoolbarconf
tmpmenubarconf = []
GSSCONF["MENUBAR_CONF"] = tmpmenubarconf
mainMenuConf = []
mainToolConf = []

def SetMenuBar(path,type,Id,helpstr,foo):
    """设置/添加某个Menu项（不存在就添加）
    """
    tmpmenubarconf.append([path,type,Id,helpstr,foo])

def RemoveMenuBar(path):
    """移除某个menu项
    """
    for i in tmpmenubarconf:
        if i[0] == path:
            tmpmenubarconf.remove(i)

def SetToolBar(name,type,Id,helpstr,foo,img=TOOLBAR_BITMAP_DEFPATH):
    """设置/添加某个Tool项（不存在就添加）
    """
    tmptoolbarconf.append([type,Id,name,img,None,helpstr,foo])

def RemoveToolBar(path,at=0):
    """移除某个Tool项
    """
    a = 0
    removeat = -1
    for i in range(len(tmptoolbarconf)):
        if tmptoolbarconf[i][2] == path:
            if at==a:
                removeat = i
            else:
                a+=1
    if removeat!=-1:
        print tmptoolbarconf.pop(removeat)

#设置默认的菜单和工具栏
SetMenuBar('DataSet/Open',UI_TYPE_BUTTON,ID_Open,"OPEN_H_STR",EDIT_MSG)
SetMenuBar('DataSet/----',UI_TYPE_SEPARATOR,None,None,None)
SetMenuBar('DataSet/Exit',UI_TYPE_BUTTON,ID_Exit,"EXIT_H_STR",EXIT_MSG)
SetMenuBar('Mode/NoMode',UI_TYPE_RADIO,[ID_NoMode,ModeKey.NoneMode],"NOMODE_H_STR",NOMODE_MSG)
SetMenuBar('Mode/Pan',UI_TYPE_RADIO,[ID_Pan,ModeKey.PanMode],"PANMODE_H_STR",PANMODE_MSG)
SetMenuBar('Mode/ZoomIn',UI_TYPE_RADIO,[ID_ZoomIn,ModeKey.ZoomInMode],"ZOOMIN_H_STR",ZOOMINMODE_MSG)
SetMenuBar('Mode/ZoomOut',UI_TYPE_RADIO,[ID_ZoomOut,ModeKey.ZoomOutMode],"ZOOMOUT_H_STR",ZOOMOUTMODE_MSG)
SetMenuBar('Mode/Info',UI_TYPE_RADIO,[ID_Info,ModeKey.InfoMode],"INFO_H_STR",INFOMODE_MSG)
SetMenuBar('Layer/Add Vector',UI_TYPE_BUTTON,ID_AddVLayer,"ADD_VLAYER_H_STR",OPENV_MSG)
SetMenuBar('Layer/Add Raster',UI_TYPE_BUTTON,ID_AddRLayer,"ADD_RLAYER_H_STR",OPENR_MSG)
SetMenuBar('Layer/Remove Selected',UI_TYPE_BUTTON,ID_RemoveLayer,"RM_LAYER_H_STR",CLOSE_MSG)


SetToolBar('Open',UI_TYPE_BUTTON,ID_Open,"OPEN_H_STR",EDIT_MSG)
SetToolBar('Save',UI_TYPE_BUTTON,ID_Save,"SAVE_H_STR",SAVE_MSG)
SetToolBar('AddVLayer',UI_TYPE_BUTTON,ID_AddVLayer,"ADD_VLAYER_H_STR",OPENV_MSG)
SetToolBar('AddRLayer',UI_TYPE_BUTTON,ID_AddRLayer,"ADD_RLAYER_H_STR",OPENR_MSG)
SetToolBar('Table',UI_TYPE_BUTTON,ID_Table,"TABLE_H_STR",TABLE_MSG)
SetToolBar('----',None,None,None,None)
SetToolBar('Full',UI_TYPE_BUTTON,ID_Full,"FULL_H_STR",FULL_MSG)
SetToolBar('----',None,None,None,None)
SetToolBar('NoMode',UI_TYPE_RADIO,[ID_NoMode,ModeKey.NoneMode],"NOMODE_H_STR",NOMODE_MSG)
SetToolBar('Pan',UI_TYPE_RADIO,[ID_Pan,ModeKey.PanMode],"PANMODE_H_STR",PANMODE_MSG)
SetToolBar('ZoomIn',UI_TYPE_RADIO,[ID_ZoomIn,ModeKey.ZoomInMode],"ZOOMIN_H_STR",ZOOMINMODE_MSG)
SetToolBar('ZoomOut',UI_TYPE_RADIO,[ID_ZoomOut,ModeKey.ZoomOutMode],"ZOOMOUT_H_STR",ZOOMOUTMODE_MSG)
SetToolBar('Info',UI_TYPE_RADIO,[ID_Info,ModeKey.InfoMode],"INFO_H_STR",INFOMODE_MSG)

RunSysConf()

def MakeMenu(menu,namearr,conf):
    if len(namearr)!=1:#弹出菜单
        submenu = []
        if len(menu)==0:
            menu.append([UI_TYPE_POPUP,namearr[0],submenu])
            MakeMenu(submenu,namearr[1:],conf)
            return
        m = [i[1] for i in menu]
        if namearr[0] in m:#已经存在该级菜单
            MakeMenu(menu[m.index(namearr[0])][2],namearr[1:],conf)
        else:#不存在该级菜单，新建
            menu.append([UI_TYPE_POPUP,namearr[0],submenu])
            MakeMenu(submenu,namearr[1:],conf)
    else:#内容
        for m in menu:
            if len(m)==1:#分割号
                continue
            if m[1]==namearr[0]:
                m[0]=conf[0];m[2]=conf[1];
                m[3]=conf[2];m[4]=conf[3]
                return
        if namearr[0]=='----':
            menu.append([UI_TYPE_SEPARATOR])
            return
        menu.append([conf[0],conf[1],namearr[0],
            conf[2],conf[3]])
        


def MakeMenuConf(tmpconf):
    for i in tmpmenubarconf:
        patharr = i[0].split('/')
        MakeMenu(mainMenuConf,patharr,i[1:])

MakeMenuConf(tmpmenubarconf)
#print mainMenuConf

def MakeToolConf(tmpconf):
    for ti in tmptoolbarconf:
        i = ti
        if i[2]=='----':
            mainToolConf.append([UI_TYPE_SEPARATOR])
            continue
        #i.append(i[5].get());i.append(i[6])
        i[5] = i[5];i[6] = i[6]
        canappend = True
        for t in mainToolConf:
            if len(t)==1:#分割号
                continue
            if i[2] == t[2]:#已经有这个工具了
                #mainToolConf[tools.index(i[2])]=i
                mainToolConf[mainToolConf.index(t)]=i
                canappend = False
                continue
        if canappend:
            mainToolConf.append(i)

MakeToolConf(tmptoolbarconf)
#print mainToolConf

#mainMenuConf2 = [
#    [UI_TYPE_POPUP,"DataSet",[
#        [UI_TYPE_BUTTON,ID_Open,"Open",OPEN_H_STR,MsgKey.MSG_KEY_EDIT],
#        #[UI_TYPE_BUTTON,ID_Table,"Table",TABLE_H_STR,':tab'],
#        [UI_TYPE_SEPARATOR],
#        [UI_TYPE_BUTTON,ID_Exit,"Exit",EXIT_H_STR,MsgKey.MSG_KEY_EXIT],
#        ]
#    ],
#    [UI_TYPE_POPUP,"Mode",[
#        [UI_TYPE_RADIO,[ID_NoMode,ModeKey.NoneMode],"NoMode",NOMODE_H_STR,'n'],
#        [UI_TYPE_RADIO,[ID_Pan,ModeKey.PanMode],"Pan",PANMODE_H_STR,'t'],
#        [UI_TYPE_RADIO,[ID_ZoomIn,ModeKey.ZoomInMode],"ZoomIn",ZOOMIN_H_STR,'Z'],
#        [UI_TYPE_RADIO,[ID_ZoomOut,ModeKey.ZoomOutMode],"ZoomOut",ZOOMOUT_H_STR,'z'],
#        [UI_TYPE_RADIO,[ID_Info,ModeKey.InfoMode],"Info",INFO_H_STR,'q'],
#        ]
#    ],
#    [UI_TYPE_POPUP,"Layer",[
#        [UI_TYPE_BUTTON,ID_AddLayer,"Add",ADD_LAYER_H_STR,MsgKey.MSG_KEY_OPEN],
#        #[UI_TYPE_BUTTON,ID_RemoveLayer,"Remove",REMOVE_LAYER_H_STR],
#        ]
#    ],
#]
#print mainMenuConf,'*'*20,'\n',mainMenuConf2
#mainToolConf2 = [
#    [UI_TYPE_BUTTON,ID_Open,"Open",TOOLBAR_BITMAP_DEFPATH,None,OPEN_H_STR,MsgKey.MSG_KEY_EDIT],
#    [UI_TYPE_BUTTON,ID_Save,"Save",TOOLBAR_BITMAP_DEFPATH,None,SAVE_H_STR,MsgKey.MSG_KEY_SAVE],
#    [UI_TYPE_BUTTON,ID_AddLayer,"AddLayer",TOOLBAR_BITMAP_DEFPATH,None,ADD_LAYER_H_STR,MsgKey.MSG_KEY_OPEN],
#    [UI_TYPE_BUTTON,ID_Table,"Table",TOOLBAR_BITMAP_DEFPATH,None,TABLE_H_STR,MsgKey.MSG_KEY_TABLE],
#    [UI_TYPE_SEPARATOR],
#    [UI_TYPE_BUTTON,ID_Full,"Full",TOOLBAR_BITMAP_DEFPATH,None,FULL_H_STR,'f'],
#    [UI_TYPE_RADIO,[ID_NoMode,ModeKey.NoneMode],"NoMode",TOOLBAR_BITMAP_DEFPATH,None,NOMODE_H_STR,'n'],
#    [UI_TYPE_RADIO,[ID_Pan,ModeKey.PanMode],"Pan",TOOLBAR_BITMAP_DEFPATH,None,PANMODE_H_STR,'t'],
#    [UI_TYPE_RADIO,[ID_ZoomIn,ModeKey.ZoomInMode],"ZoomIn",TOOLBAR_BITMAP_DEFPATH,None,ZOOMIN_H_STR,'Z'],
#    [UI_TYPE_RADIO,[ID_ZoomOut,ModeKey.ZoomOutMode],"ZoomOut",TOOLBAR_BITMAP_DEFPATH,None,ZOOMOUT_H_STR,'z'],
#    [UI_TYPE_RADIO,[ID_Info,ModeKey.InfoMode],"Info",TOOLBAR_BITMAP_DEFPATH,None,INFO_H_STR,'q'],
#]
#print mainToolConf,'*'*20,'\n',mainToolConf2
