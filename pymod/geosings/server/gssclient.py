from socket import *
import sys

import re
from Numeric import *
ADDR = 'localhost'
PORT = 2386

def sendraw(data):
    sendSock = socket(AF_INET,SOCK_STREAM)
    sendSock.connect((ADDR,PORT))
    sendSock.send(data+'\r\n')
    #fp = file('data.txt', 'wb')
    while 1:
        text = sendSock.recv(200)
        #print text
        if text:
            #fp.write(text)
            print 'rec:',text,'/end:'
            gps = re.split('\n|\r\n',text)
            print gps
            arr = fromstring(gps[1],Int32)
            print arr
            print 'exit'
            break
        else:
            print 'exit'
            break
    sendSock.close()
    sys.exit()
    #fp.close()

if __name__ == '__main__':
    url = raw_input('input:')
    sendraw(url)
