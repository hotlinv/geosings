# -*- encoding: utf-8 -*-
"""
定义日志模块

 - writer:linux_23; create: 2008.4.7; version:1; 创建
"""
import UseGetText
from EncodeTran import *
from RunSysConf import RunSysConf
from GssConfDict import GSSCONF
from geosings.core.system import choose

import logging,types

RunSysConf()

class ConsoleStreamHandler(logging.StreamHandler):
    def __init__(self, strm=None):
        logging.StreamHandler.__init__(self, strm)
    def emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline
        [N.B. this may be removed depending on feedback]. If exception
        information is present, it is formatted using
        traceback.print_exception and appended to the stream.
        """
        try:
            msg = self.format(record)
            fs = "%s\n"
            self.stream.write(fs % utf82locale(msg))
            self.flush()
        except:
            self.handleError(record)


class GLogging:
    def __init__(self,initConsole=True):
        dlevel = GSSCONF['debug']
        self.level = level = choose(dlevel,logging.DEBUG,logging.INFO)
        logging.getLogger('').setLevel(level)
        if initConsole:
            self.regStreamHandler(level)
        logging.addLevelName(100,_('message'))

    def getLevel(self):
        return self.level

    def regStreamHandler(self, level, stream=None):
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = ConsoleStreamHandler(stream)
        console.setLevel(level)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s- %(levelname)-8s: %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

    def regHandler(self, handler, level):
        if level is not None:
            handler.setLevel(level)
        formatter = logging.Formatter('%(name)-6s- %(levelname)-8s: %(message)s')
        # tell the handler to use this format
        handler.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(handler)

    def regFileHandler(self, level, filename, mode='w'):
        # define a Handler which writes INFO messages or higher to the sys.stderr
        file = logging.FileHandler(filename, mode)
        file.setLevel(level)
        # set a format which is simpler for file use
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        # tell the handler to use this format
        file.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(file)

    def log(self, what=''):
        return logging.getLogger(what)

_GLOG = GLogging()

#定义不同的level的函数
debug = _GLOG.log().debug
info = _GLOG.log().info
error = _GLOG.log().error
warning = _GLOG.log().warning
cirtical = _GLOG.log().critical
order = lambda what: _GLOG.log().log(100, what)

glog = lambda what: _GLOG.log(what)

register_log_handler = lambda what,level=_GLOG.getLevel():_GLOG.regHandler(what,level)

if __name__=="__main__":
    import sys
    info('begin')
    debug('debug一个 %s',dir(sys))
    warning('警告一个')
    _GLOG.regFileHandler(logging.DEBUG,'./geosings.log','a')
    order(u'命令')
    glog('funhoo').warning('Jail zesty vixen who grabbed pay from quack.')
    glog('funhoo').error('The five boxing wizards jump quickly.')
    gsslog = glog('geosings')
    gsslog.warning('Quick zephyrs blow, vexing daft Jim.')
    gsslog.debug('Quick zephyrs blow, vexing daft Jim.')
    gsslog.info('How quickly daft jumping zebras vex.')

