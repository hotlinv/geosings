#! /usr/bin/env python

import os, shutil, sys, os.path

print '*'*40,'\n'*3,'Welcome to GeoSings Control Center','\n'*3,'*'*40
GSSHOME=os.path.split(__file__)[0]
print GSSHOME

if os.name == 'nt':
    SYST='win'
else:
    SYST='unix'

runapp='app'
runtools='tools'
showdoc='doc'
runmakedoc='mkdoc'
maketags='mktags'
runprj='prj'
runweb='webpub'
runweblc='weblc'
runinitdb='initdb'
rundbshell='dbshell'

args = [runapp,runtools,showdoc,runmakedoc,maketags,
        runprj,runweb,runweblc,
        runinitdb,rundbshell]

tagscmd = """ctags -R --language-force=Python --format=1 --file-scope=yes --exclude=.svn .."""
mkdocwcmd = """epydoc.py --no-imports %s --debug --html -o "../../docs/%s" %s"""
mkdocucmd = """epydoc --html -o "../../docs/%s" %s"""
docwcmd = """start %s index.html"""
docucmd = """firefox index.html &"""
webpubcmd = """python manage.py runserver %s:8000"""
weblccmd = """python manage.py runserver"""
initdbcmd = """python manage.py syncdb"""
dbshcmd = """python manage.py shell"""

def runNewRootProcess(cmd):
    try:
        forkPID = os.fork()
    except:
        raise "unable create new process."
    if forkPID >0 :# parent process
        return
    elif forkPID == 0:#new child process
        os.setsid()# move process to pstree root
        os.system(cmd)

def printhelp(opt=''):
    argstr = '{'+" | ".join(args)+'}'+"\ndefault:"+runapp
    if opt=='args':
        print "select a operator as following: \n%s" % argstr
    else:
        print "Usage: %s " % argstr

def getIpAddress():
    import socket
    return socket.gethostbyname(socket.gethostname())


def mktags():
    os.chdir(os.path.join(GSSHOME,'pymod'))
    print 'makeing geosings tags...'
    os.system(tagscmd)
    shutil.move('./tags',"../tools/tags")
    print 'success!'
    
def runproject ():
    print 'Running Project...'
    if SYST=='win' :
        os.system("cmd /c start pythonw ProjectCtrl.py")
        #execfile('./ProjectCtrl.pyw')
        sys.exit(0)
    else:  # Unix
        runNewRootProcess("python ProjectCtrl.py &")
        sys.exit(0)

def selectbool(order,s1,s2):
    output = "%s (%s/%s) : " % (order, s1, s2)
    sel = raw_input(output)
    if len(sel)==0: sel = s1
    return sel

def makedoc(which, isall,isquiet):
    if isall!='y':
        ismake = selectbool('make %s?' % which,'y','n')
    else:
        ismake = 'y'
    if ismake == 'y':
        print 'making gss_%s docs...' % which
        docname = 'gss_%s' % which
        if SYST=='win': os.system(mkdocwcmd % (isquiet,docname,which))
        else: os.system(mkdocucmd % (docname,which))
    else:
        print 'ignore gss_%s' % which

def mkdocs():
    isquiet = selectbool('quiet?','n','y')
    if isquiet != 'y': quiet='-v'
    else: quiet='-q'
    if SYST != 'win':
        if isquiet != 'y':
            quiet = ' --debug'
        else:
            quiet = ""

    isall = selectbool("all?",'y','n')
    if isall=='y': print 'making all doc...'
    
    makedoc('core',isall,isquiet)
    makedoc('ui',isall,isquiet)
    makedoc('tools',isall,isquiet)

    print 'Done!'

def showdocs():
    if SYST == 'win':
        etype = raw_input('select a explorer : ')
        if len(etype)==0:
            print 'Calling default internet explorer to show docs...'
        os.system(docwcmd % etype)
        sys.exit(0)
    else:
        print 'using www-browser'
        os.system(docucmd)
        sys.exit(0)

def quit():
    e = raw_input('press any key to exit...')

def Usage():
    printhelp()
    quit()

def runwebsev ():
    os.chdir(os.path.join(GSSHOME,'webgss','funhoo'))
    os.system(webpubcmd % getIpAddress())

def runlcwebsev ():
    os.chdir(os.path.join(GSSHOME,'webgss','funhoo'))
    os.system(weblccmd)

def runinidb ():
    os.chdir(os.path.join(GSSHOME,'webgss','funhoo'))
    os.system(initdbcmd)

def rundbsh ():
    os.chdir(os.path.join(GSSHOME,'webgss','funhoo'))
    os.system(dbshcmd)

if __name__ == '__main__':
    printhelp('args')
    if len(sys.argv)==1:
        input = raw_input('input here:')
        if len(input)==0: 
            #printhelp()
            #sys.exit(1)
            input=runapp
    else:
        input = sys.argv[0]

    if input==runapp:
        os.chdir(os.path.join(GSSHOME,'bin'))
        os.system('python gssapp.py')
    elif input == runtools:
        os.chdir(os.path.join(GSSHOME,'bin'))
        os.system("python gssapp.py lin")
    elif input == runprj:
        os.chdir(os.path.join(GSSHOME,'tools'))
        runproject()
    elif input == showdoc:
        os.chdir(os.path.join(GSSHOME,'docs'))
        showdocs()
    elif input == runmakedoc:
        os.chdir(os.path.join(GSSHOME,'pymod','geosings'))
        mkdocs()
    elif input == maketags:
        mktags()
    elif input == runweb:
        runwebsev()
    elif input == runweblc:
        runlcwebsev()
    elif input == runinitdb:
        runinidb()
    elif input == rundbshell:
        rundbsh()
    else :
        Usage()
        sys.exit(1)
    
    quit()
    sys.exit(0)
