#!/usr/bin/env python

import os, os.path, sys, shutil

thisdir = os.listdir('.')
if "projctrl.conf" not in thisdir:
    print "create configure file porject.conf ..."
    shutil.copyfile("projctrl.conf.template", "projctrl.conf")
else:
    print "projctrl.conf exist! pass ..."

if not os.access("./Session.vim",os.F_OK):
    try:
        print 'create Session for vim editor ...'
        os.system('vim -c mksession -c q')
    except:
        print 'warning: You should edit the projctrl.conf by yourself!'
else:
    print "Session.vim exist! pass ..."

pwd = os.getcwd()
os.chdir('./lang')
langdir = os.listdir('.')
for po in langdir:
    if not po.endswith('.po'):
        continue
    else:
        poname = os.path.splitext(po)[0]
        moname = poname+'.mo'
    if moname not in langdir:
        pyhome = sys.prefix
        if os.name == 'nt':
            msgfmt = os.path.join(pyhome,'Tools','i18n','msgfmt.py')
            torun = msgfmt+' '+po
        else:
            msgfmt = 'msgfmt'
            torun = " ".join([msgfmt,po,"-o "+moname])
        print "run msgfmt.py to create %s file ..." % moname
        os.system(torun)
    else:
        print "language file %s exist! pass ..." % po
os.chdir(pwd)

print 'success!'
test = raw_input('press any key to continue...')
