
from apihelper import MemberParser
import codecs
class IsNotModuleE(Exception):pass

def getHtmlText(body):
    return """
    <html>
    <head>
        <style type='text/css'>
            @import url("function.css");
        </style>
    </head>
    <body>
    %s
    </body>
    </html>
    """ % body

class ModuleDocHtmlMaker:
    def __init__(self,context):
        self.html = ""
        self.context = context
    def getHtml(self):
        self.html = getHtmlText(self.__getModuleContext(self.context))
        return self.html
    def __getModuleContext(self,context):
        if context['type'] != 'module':
            raise IsNotModuleE
        name = context['name']
        doc = context['doc']
        member = context['members']
        classes = member['classes']
        funcs = member['functions']
        return '<br />'.join([
                    self.__getModuleText(name,doc),
                    self.__getClassListText(classes),
                    self.__getFunctionText(funcs),
                    self.__getClassText(classes),
                ])

    def __getClassText(self,classes):
        pass
    
    def __getModuleText(self,name,doc):
        return """
        <p><h1>Module: %s </h1>%s</p>
        """ % (name,doc)

    def __getFunctionText(self,fs):
        ftabdata = '\n'.join(["""<tr><td class='fun_tab_data'>%s</td></tr>""" %
            (i['body']) for i in fs])
        return """
        <table class="fun_table">
            <tr class="fun_tab_head">
                <th class='fun_tab_head'> Functions </th>
            </tr>
            %s
        </table>
        """ % ftabdata

    def __getClassListText(self,classes):
        ctabdata = '\n'.join(["""<tr><td class='fun_tab_data'>%s</td><td
            class='fun_tab_data'>%s</td></tr>""" %
            (i['name'],i['doc']) for i in classes])
        return """
        <table class="fun_table">
            <tr class="fun_tab_head">
                <th class='fun_tab_head'> Classes </th>
                <th class='fun_tab_head'> .</th>
            </tr>
            %s
        </table>
        """ % ctabdata


def MakeDoc(module,oppath):
    mp = MemberParser()
    context = mp.Parse(module)
    mm = ModuleDocHtmlMaker(context)
    f = codecs.open(oppath,'w','utf-8')
    h = mm.getHtml()
    #print h
    f.write(h)
    f.close()
    
if __name__== '__main__':
    import GeoRect
    MakeDoc(GeoRect,"api.html")
