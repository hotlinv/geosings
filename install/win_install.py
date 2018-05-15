# -*- encoding: utf-8 -*-
import os
def getvnum(numstr):
    arr = [int(i) for i in numstr.split('.')]
    return arr[0]*10000+arr[1]*100+arr[2]

def cmpvnum(num1,num2):
    if num1>num2: return 1
    elif num1==num2: return 0
    else: return -1

def filenum(file,version):
    f = open(file)
    infos = []
    line = f.readline()
    while line:
        line = line.strip()
        if line.startswith('*'):
            print "version", version,getvnum(line[1:])
            if cmpvnum(version,getvnum(line[1:]))<0:
                break
            else:
                infos = []
                line = f.readline()
        else:
            if line != "":
                infos.append(line.split(' '))
                line = f.readline()
    f.close()
    return infos

print u'正在下载所依赖的Python软件包...'
pkgslist = 'pkgs.list2'
if os.access(pkgslist,os.F_OK):
    os.remove(pkgslist)
os.system('wget '+"http://www.cnforge.org/svnroot/geosings/"+pkgslist)

thisfile = os.path.split(os.path.abspath(__file__))[0]
parentfile = os.path.split(thisfile)[0]

vfile = open(os.path.join(parentfile,'version'))
vnum = getvnum(vfile.readline().strip())
vfile.close()
infos = filenum(pkgslist, vnum)
if infos == None:
    print u'版本读取错误！程序停止。'
    import sys
    sys.exit(1)

print "%"*30
print infos
print "%"*30

for info in infos:
    #print info
    pkgname = info[0]; pkgurl = info[1]
    if not os.access(pkgname, os.F_OK):
        print u"正在下载"+pkgname+"..."
        os.system(r'wget "%s"' % pkgurl)
    if os.access(pkgname, os.F_OK):
        print u'正在解压'+pkgname+'...'
        try:
            os.system("unzip -q -n "+pkgname)
        except:
            print u"解压失败，但程序继续，后面的操作可能失败！"

print u'现在开始安装...'

print u'开始安装依赖包...'

execfile('inst_pkgs.py')
execfile('install_gdal.py')

print u'设置环境变量...'
import regenv

pymod = os.path.join(parentfile,'pymod')
keyname = 'PYTHONPATH'
regenv.regOSEnv(keyname, pymod)

import sys
pyhome = sys.prefix
pathkey = "PATH"
regenv.regOSEnv(pathkey,pyhome)

pwd = os.getcwd()
gssbinpath = os.path.join(os.path.split(pwd)[0],'bin')
regenv.regOSEnv(pathkey,gssbinpath)

print "==============================================================="
print u"好的，安装结束，现在重启机器，并运行runGeosings.py并键入app来运行主程序!"
