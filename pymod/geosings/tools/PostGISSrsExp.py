# -*- coding: utf-8 -*-
#writer:linux_23; create: 2007.6.23; version:1; 创建
"""
该模块定义PostGIS坐标系统的导出
"""

import os,re

class PostGISSrsExp:
    def __init__(self,pgconf):
        """初始化
        @type pgconf: dict
        @param pgconf:
        PostGIS的配置字典，包括下面几项
            （只要连得上，省略几项也可以）
            -pgbin: psql可执行程序位置
            -host: 主机位置
            -port: 端口
            -user: 用户名
            -pwd: 密码
            -geodb: 有空间参考列表的数据库
        """
        self.pgconf = pgconf

    def ExpToTxt(self,opath):
        os.environ["PGUSER"]=self.pgconf['user']
        os.environ["PGPASSWORD"]=self.pgconf['pwd']
        psqlbin = os.path.join(self.pgconf["pgbin"],"psql")
        if os.path.isdir(opath):
            tmptxt = os.path.join(opath,"srs.txt")
            os.system(psqlbin+" -d " + self.pgconf['geodb'] +
                    ' -U ' + self.pgconf['user']+
                    ' -c "select * from spatial_ref_sys;" -o "'+
                    tmptxt + '"')
            self.__ExpToTxts(opath,"srs.txt")
        else:
            os.system(psqlbin+" -d " + self.pgconf['geodb'] +
                    ' -U ' + self.pgconf['user']+
                    ' -c "select * from spatial_ref_sys;" -o "'+
                    opath + '"')

    def __ExpToTxts(self, opath, srsfname):
        file = open(os.path.join(opath, srsfname))
        line = file.readline()
        srss = []
        while(line):
            restr = r'^\s*(\d+)\s*\|\s*(\w+)\s*\|\s*(\d+)\s*\|(.+)\|.+$'
            m = re.match(restr,line)
            if m is None:
                line = file.readline()
                continue
            srsg = m.groups()
            #if srs[1] is not None:
            #print srs[3]
            srs = srsg[3]
            res2 = r'^\s*\w+\["([^"]+).+$'
            m2 = re.match(res2,srs)
            nameg = m2.groups()
            name = nameg[0]
            #name = name.replace('/','-')
            names = [n.strip() for n in name.split('/') if n != ""]
            ofilename = opath
            for n in names:
                ofilename = os.path.join(ofilename,n)
            if len(names)>1:
                try:
                    tmpdir = os.path.split(ofilename)[0]
                    os.makedirs(tmpdir)
                except Exception,e:
                    pass

            ofile = open(ofilename+'.prj','w')
            ofile.write(srs.strip())
            ofile.close()
            print 'export ',name,' ...'
            line = file.readline()

if __name__=="__main__":
    pgconf = {
            "pgbin":"D:/ProgramFiles/PostgreSQL/8.2/bin",
            "user":"postgres",
            "pwd":"postgres",
            "geodb":"geodb",
            }
    srsexp = PostGISSrsExp(pgconf)
    srsexp.ExpToTxt("d:/gisdata/sr.txt")
