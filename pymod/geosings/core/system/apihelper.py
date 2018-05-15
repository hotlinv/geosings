import inspect,re

getDocStr = lambda s: str(s)

class MemberParser:
    paramrestr = r'^@\s*param\s+(.+):(.+)$'
    typerestr = r'^@\s*type\s+(.+)\s*:\s*(.+)$'
    rtrestr = r''
    retrestr = r''
    def __init__(self,object = None):
        self.obj = object
        if object is not None:self.Parse(object)

    def Parse(self,object):
        if object is None: object = self.obj
        context = None
        if inspect.ismodule(object):
            context = self.ParseModule(object)
        elif inspect.isclass(object):
            context = self.ParseClass(object)
        elif inspect.ismethod(object):
            context = self.ParseMethod(object)
        elif inspect.isfunction(object):
            context = self.ParseFunction(object)
        return context
    def ParseModule(self,module):
        return {'type':'module',
                'name':module.__name__,
                'doc':getDocStr(module.__doc__).decode('utf-8'),
                'members':{
                    "classes":[self.ParseClass(c[1]) for c in
                        self.getMember(module,inspect.isclass)],
                    "functions":[self.ParseFunction(f[1]) for f in
                        self.getMember(module,inspect.isfunction)],
                    },
                }
    def ParseClass(self,c):
        return {'type':'class',
                'name':c.__name__,
                'doc':getDocStr(c.__doc__).decode('utf-8'),
                'members':{
                    "method":[self.ParseMethod(m[1]) for m in
                        self.getMember(c,inspect.ismethod)],
                    },
                }
    def ParseMethod(self,m):
        doc,param,ret = self.ParseDoc(m.__doc__)
        return {"type":'method',
                'name':m.__name__,
                'body':"".join([m.__name__,self.getMethodObjArgsStr(m)]),
                'doc':getDocStr(doc).decode('utf-8'),
                'members':{
                    "params":param,
                    "return":ret,
                    },
                }
    def ParseFunction(self,fun):
        doc,param,ret = self.ParseDoc(fun.__doc__)
        return {"type":'function',
                "name":fun.__name__,
                "body":"".join([fun.__name__,self.getMethodObjArgsStr(fun)]),
                "doc":getDocStr(doc).decode('utf-8'),
                'members':{
                    "params":param,
                    'return':ret,
                    },
                }
    def ParseDoc(self,doc):
        if doc is None: return [None,None,None]
        at = doc.find('@')
        if(at==-1):return [doc,None,None]
        else:
            doc,left = doc[0:at-1],doc[at:]
            leftarr = [i.strip() for i in left.split('\n')]
            paramdict = {}
            retarr = [None,""]
            for i in leftarr:
                if i.startswith('@param'):
                    m = re.match(MemberParser.paramrestr,i)
                    gs = m.groups()
                    if gs[0] in paramdict:
                        paramdict[gs[0]][1] = gs[1]
                    else:
                        paramdict[gs[0]] = ['',gs[1]]
                elif i.startswith('@type'):
                    m = re.match(MemberParser.typerestr,i)
                    gs = m.groups()
                    if gs[0] in paramdict:
                        paramrestr[gs[0]][0] = gs[1]
                    else:
                        paramdict[gs[0]] = [gs[1],'']
                elif i.startswith('@return'):
                    retarr[1] = i.split(':')[1].strip()
                elif i.startswith('@rtype'):
                    retarr[0] = i.split(':')[1].strip()
            return [doc,paramdict,retarr]

    def getMember(self,object,boolfun):
        return [i for i in inspect.getmembers(object) if boolfun(i[1])]

    def getFunctionList(self,object):
        #print inspect.getmembers(object)
        return [i for i in inspect.getmembers(object) if
            inspect.isfunction(i[1])]

    def getMethodList(self,object):
        #print [type(i[1]) for i in inspect.getmembers(object)]
        return [i for i in inspect.getmembers(object) if
            inspect.ismethod(i[1])] 

    def getMethodWholeNameList(self,object):
        mets = getMethodList(object)
        return ["".join([i[0],getMethodArgsStr(i)]) for i in mets]

    def getMethodArgsStr(self,method):
        #print method
        return inspect.formatargspec(*inspect.getargspec(method[1]))
    def getMethodObjArgsStr(self,method):
        #print method
        #print type(method)
        try:
            return inspect.formatargspec(*inspect.getargspec(method))
        except:
            return ''

def info(object, spacing=10, collapse=1): 
    """Print methods and doc strings.
    
    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object,
                           method).__doc__).decode('utf-8')))
                     for method in methodList])

if __name__ == "__main__":    
    mp = MemberParser()
    import FillLine
    print mp.Parse(FillLine)
    #print mp.Parse(FillLine.FillLine)
    #print mp.Parse(FillLine.FillLine.GetLine)
    #import GeoRect
    #print mp.Parse(GeoRect)
    #print mp.Parse(GeoRect.GetGeoRectGeometry)
    #print info.__doc__
    #import Layer
    #print mp.Parse(Layer)

