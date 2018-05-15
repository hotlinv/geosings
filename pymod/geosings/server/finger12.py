from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic
class FingerProtocol(basic.LineReceiver):
    def connectionMade(self): 
        self.transport.write("Hello 79!\n")
    def lineReceived(self, user):
        #self.transport.write('receive:'+user)
        #self.transport.write('\n'+self.users)
        self.factory.getUser(user
        ).addErrback(lambda _: "Internal error in server"
        ).addCallback(lambda m:
                      (self.transport.write(m+"\r\n"),
                       self.transport.write( usr )))#,
                       #self.transport.loseConnection()))

class FingerFactory(protocol.ServerFactory):
    protocol = FingerProtocol
    def __init__(self, **kwargs): self.users = kwargs
    def getUser(self, user):
        #protocol.transport.write(user)
        return defer.succeed(self.users.get(user, "No such user"))

class FingerSetterProtocol(basic.LineReceiver):
    def connectionMade(self): 
        self.lines = []
        self.transport.write("Hello!\n")
    def lineReceived(self, line): 
        self.lines.append(line)
        self.transport.write('receive:')
    def connectionLost(self, reason):
        self.factory.setUser(*self.lines[:2])
        # first line: user    second line: status

class FingerSetterFactory(protocol.ServerFactory):
    protocol = FingerSetterProtocol
    def __init__(self, ff): 
        self.setUser = ff.users.__setitem__

ff = FingerFactory(moshez='Happy and well')
fsf = FingerSetterFactory(ff)

application = service.Application('finger', uid=1, gid=1)
serviceCollection = service.IServiceCollection(application)
internet.TCPServer(79,ff).setServiceParent(serviceCollection)
internet.TCPServer(1079,fsf).setServiceParent(serviceCollection)
