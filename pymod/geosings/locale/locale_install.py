#! /usr/bin/env python
import os, sys

if os.name == 'nt':
    pyhome = sys.prefix
    msgfmt = os.path.join(pyhome,'Tools','i18n','msgfmt.py')
else:
    msgfmt = 'msgfmt'

langdirarr = os.listdir('.')
for langdir in langdirarr:
    if os.path.isdir(langdir):
        print 'cd dir',langdir
        pwd = os.getcwd()
        os.chdir(langdir) 
        files = os.listdir('.')
        for po in files:
            if not po.endswith('.po'):
                continue
            else:
                poname = os.path.splitext(po)[0]
                moname = poname+'.mo'
            if moname not in files:
                if os.name=='nt':
                    torun = msgfmt+' '+po
                else:
                    torun = " ".join([msgfmt,po,"-o "+moname])
                print "\trun msgfmt.py to create %s file ..." % moname
                os.system(torun)
            else:
                print "\tlanguage file %s exist! pass ..." % po
        os.chdir(pwd)

