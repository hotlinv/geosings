from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic
from Numeric import *
def ParseOrder(msg):
    if msg == 'test':
        print 'return a array!'
        a = array([123,456,0,911],Int32)
        return a.tostring()

class GssProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.transport.write('Hello !\n')
    def lineReceived(self, order):
        self.factory.Action(order
        ).addErrback(lambda _: 
                    self.transport.write("Internal error in server")
        ).addCallback(lambda m:
                   (self.transport.write(m+'\r\nend\r\n')))

class GssFactory(protocol.ServerFactory):
    protocol = GssProtocol
    def __init__(self): pass
    def Action(self,order):
        print(order)
        ret = ParseOrder(order)
        print ret
        return defer.succeed(ret)

gf = GssFactory()

application = service.Application('gssservice', uid=1, gid=1)
serviceCollection = service.IServiceCollection(application)

internet.TCPServer(2386,gf).setServiceParent(serviceCollection)
