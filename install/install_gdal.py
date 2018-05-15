
import sys,os,shutil
pyhome = sys.prefix

gdal_homename = 'gdal-1.4.0'

sitepkgs = os.path.join(pyhome,'Lib','site-packages')
gdalsite = os.path.join(sitepkgs, gdal_homename)
if not os.access(gdalsite,os.F_OK):
    print 'make gdal home'
    os.makedirs(gdalsite)

thispath = os.path.split(os.path.abspath(__file__))[0]

gdalpath = os.path.join(thispath, 'gdal140')
gdalexpath = os.path.join(thispath, 'gdal140ext')
bindir = os.path.join(gdalpath, 'bin')
print bindir
pymoddir = os.path.join(gdalpath, 'pymod')

pwd = os.getcwd()

gssbinpath = os.path.join(os.path.split(pwd)[0],'bin')

os.chdir(bindir)
os.system('copy * '+gssbinpath)
os.chdir(pymoddir)
os.system('copy * '+gdalsite)
os.chdir(gdalexpath)
os.system('copy * '+gssbinpath)

os.chdir(pwd)

f = open(os.path.join(sitepkgs,'gdal.pth'),'w')
f.write(gdal_homename)
f.close()
#shutil.copy(binfiles, gdalsite)

