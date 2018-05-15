# -*- coding: utf-8 -*-
"""
模块定义ui中的常数和枚举值
"""
import wx

class ActionResult:
    """运行命令的结果
    """
    Successed = 2
    UpdateAll = 1
    Failuse = 0

class ModeKey:
    """模式的值
    """
    NoneMode = 0
    ZoomOutMode = 1
    ZoomInMode = 2
    PanMode = 3
    EditMode = 4
    InfoMode = 5

modeMap = {
        ModeKey.NoneMode:'No Mode',
        ModeKey.ZoomOutMode:'ZoomOut Mode',
        ModeKey.ZoomInMode:'ZoomIn Mode',
        ModeKey.PanMode:'Pan Mode',
        ModeKey.EditMode:'Edit Mode',
        ModeKey.InfoMode:'Info Mode'
        }

TOOLBAR_BITMAP_DEFW = 22
TOOLBAR_BITMAP_DEFH = 22
TOOLBAR_BITMAP_DEFSIZE = wx.Size(TOOLBAR_BITMAP_DEFW,
        TOOLBAR_BITMAP_DEFH)

TOOLBAR_BITMAP_DEFPATH = 999

UI_TYPE_SEPARATOR = 1000
UI_TYPE_BUTTON = 1001
UI_TYPE_RADIO = 1002
UI_TYPE_CHECK = 1003
UI_TYPE_POPUP = 1004

def GetUIWxType(type):
    if type == UI_TYPE_BUTTON:
        return wx.ITEM_NORMAL
    elif type == UI_TYPE_RADIO:
        return wx.ITEM_RADIO

#下面是MenuBar的对应ID
ID_Open = 10001
ID_Save = 10002
ID_Table = 10003
ID_Exit = 10004
ID_NoMode = 10100
ID_Pan = 10101
ID_ZoomIn = 10102
ID_ZoomOut = 10103
ID_Info = 10104
ID_AddVLayer = 10201
ID_AddRLayer = 10202
ID_RemoveLayer = 10203
ID_Full = 10204

#下面是ToolBar的对应ID
#ID_TB_Open = 20001
#ID_TB_Save = 20002
#ID_TB_AddLayer = 20003
#ID_TB_NoMode = 20100
#ID_TB_Pan = 20101
#ID_TB_ZoomIn = 20102
#ID_TB_ZoomOut = 20103
#ID_TB_Info = 20104



