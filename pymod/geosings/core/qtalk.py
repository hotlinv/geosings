# -*- encoding: utf-8 -*-
import xmpp
import pydoc

login = 'linux23maillist' # @gmail.com
pwd   = 'linux23'
friend = 'lilin.maillist@gmail.com'

cnx = xmpp.Client('gmail.com')
cnx.connect( server=('talk.google.com',5223) )

cnx.auth(login,pwd, 'li lin')
cnx.sendInitPresence()


cnx.send( xmpp.Message( friend ,u"我来了！娃花花花花……\n\n\n来，先刷屏一下..." ) )
def messageCB(conn,msg):
    print '******************************'
    print "from: " + unicode(msg.getFrom())
    body = unicode(msg.getBody())
    print "Content: " + body
    if body == u"滚":
        conn.send( xmpp.Message( friend ,u"好吧，我走了，88" ) )
        import sys
        sys.exit(0)
    elif body.startswith('dir '):
        sb = body.split()
        sbs = sb[1].split('.')
        pkg, name = '.'.join(sbs[:-1]), sbs[len(sbs)-1]
        exec "from "+pkg+" import "+name
        try:
            e = eval("dir("+name+")")
            conn.send( xmpp.Message(friend, e))
        except:
            conn.send(xmpp.Message(friend, u"命令有错!"))
    elif body.startswith('doc '):
        sb = body.split()
        sbs = sb[1].split('.')
        pkg, name = '.'.join(sbs[:-1]), sbs[len(sbs)-1]
        exec "from "+pkg+" import "+name
        try:
            e = eval(name+".__doc__")
            conn.send( xmpp.Message(friend, e))
        except:
            conn.send(xmpp.Message(friend, u"命令有错!"))
    elif body.startswith('help '):
        sb = body.split()
        sbs = sb[1].split('.')
        pkg, name = '.'.join(sbs[:-1]), sbs[len(sbs)-1]
        exec "from "+pkg+" import "+name
        try:
            e = eval("pydoc.getdoc("+name+")")
            conn.send( xmpp.Message(friend, e))
        except:
            conn.send(xmpp.Message(friend, u"命令有错!"))
    else:
        conn.send( xmpp.Message(friend ,u"收到："+body ) )
    print '******************************'

cnx.RegisterHandler('message', messageCB)

def StepOn(conn):
    try:
        conn.Process(1)
    except :
        return 0
    return 1
def GoOn(conn):
    while StepOn(conn):
        pass


GoOn(cnx)
