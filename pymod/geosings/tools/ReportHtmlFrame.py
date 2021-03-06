﻿# -*- coding: utf-8 -*-
"""作为Html报表生成的模板
"""

#<?xml version="1.0" encoding="UTF-8"?>
#<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
#       "http://www.w3.org/TR/xhtml11/DTD/xhtml11-transitional.dtd">
#<html xmlns="http://www.w3.org/1999/xhtml">
#<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
HTMLFRAME = u"""
<html>
<head>
  <title>
  	%s
  </title>
  <script type="text/javascript" src="/js/layerinfo.js">
  </script>
  <link rel="stylesheet" type="text/css" href="/css/layerinfo.css" />
</head>
<body onload='load();'>
  <center>
     <h1>%s</h1>
  </center>
  %s
</body>
</html>
"""
def GetHTMLFrame(heart,title,body):
    """获取HTML的节点框架
    @type heart: str
    @param heart: 头节点的内容
    @type title: str
    @param title: 网页名字
    @type body: str
    @param body: 网页主要内容的名字
    @rtype: str
    @return: html字符串内容
    """
    return HTMLFRAME % (heart,title,body)

HR = "<hr>"

H2FRAME = """
<h2>%s</h2>
"""
def GetH2(content):
    """形成H2节点的内容
    @type content: str
    @param content: h2节点内容
    @rtype: str
    @return: html字符串内容
    """
    return H2FRAME % content

H3FRAME = """
<h3>%s</h3>
"""

def GetH3(content):
    """形成h3节点的内容
    @type content: str
    @param content: h3节点内容
    @rtype: str
    @return: html字符串内容
    """
    return H3FRAME % content

LISTFRAME = """
<ul>
   %s 
</ul>
"""
def GetListFrame(content):
    """形成ul列表节点的框架
    @type content: str
    @param content: ul列表内容
    @rtype: str
    @return: html字符串内容
    """
    return LISTFRAME % content

OLFRAME = """
<ol>
 %s
</ol>
"""
def GetOLFrame(content):
    """形成ol列表节点的框架
    @type content: str
    @param content: ol列表内容
    @rtype: str
    @return: html字符串内容
    """
    return OLFRAME % content

LIFRAME = """
 <li>%s</li>
"""
def GetLiFrame(content):
    """形成li列表节点的框架
    @type content: str
    @param content: li列表内容
    @rtype: str
    @return: html字符串内容
    """
    return LIFRAME % content

def GetTH(col):
    """形成th表头节点
    @type col: str
    @param col: th列表内容
    @rtype: str
    @return: html字符串内容
    """
    return "<th>%s</th>" % col

def GetTabHead(cols):
    """形成tr表头节点
    @type cols: list
    @param cols: 列表头节点列表
    @rtype: str
    @return: html字符串内容
    """
    colstrs = []
    for c in cols:
        colstrs.append(GetTH(c))
    thstr = "".join(colstrs)
    return '<tr>%s</tr>' % thstr

def GetTableVal(vals):
    """形成表数据
    @type vals: list
    @param vals: 列表数据
    @rtype: str
    @return: html字符串内容
    """
    tds = []
    for v in vals:
        tr = ['<tr>']
        for f in v:
            tr.append('<td>%s</td>' % str(f))
        tr.append('</tr>')
        tds.append(''.join(tr))
    return ''.join(tds)



#############################################################

from xml.dom.minidom import *

doc = Document()

def GetHead(cols):
    """形成tr表头节点，用dom创建
    @type cols: list
    @param cols: 列表头节点列表
    @rtype: str
    @return: html字符串内容
    """
    tr = doc.createElement('tr')
    for c in cols:
        th = doc.createElement('th')
        t = doc.createTextNode(c)
        th.appendChild(t)
        tr.appendChild(th)
    return tr 

def GetVals(vals):
    """形成表数据，用dom创建
    @type vals: list
    @param vals: 列表数据
    @rtype: str
    @return: html字符串内容
    """
    valnodes = []
    for v in vals:
        tr = doc.createElement('tr')
        for f in v:
            td = doc.createElement('td')
            d = doc.createTextNode(str(f))
            td.appendChild(d)
        tr.appendChild(td)
        valnodes.append(tr)
    return valnodes

def GetTable(cols,vals):
    """形成表数据
    @type cols: list
    @param cols: 列表表头
    @type vals: list
    @param vals: 列表数据
    @rtype: str
    @return: html字符串内容
    """
    tabstr = ["<table>"]
    tabstr.append( GetTabHead(cols) )
    tabstr.append( GetTableVal(vals) )
    tabstr.append( '</table>' )
    return ''.join(tabstr)
    #colsnode = GetHead(cols)
    #valnodes = GetVals(vals)
    #table = doc.createElement('table')
    #table.appendChild(colsnode)
    #for n in valnodes:
    #    table.appendChild(n)
    #return table.toxml()
