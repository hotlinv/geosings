from _winreg import *
import os

env = os.environ

def regkey(key,envkey,keyname,value):
    if keyname not in env:
        CreateKey(key,envkey)
        k = OpenKey(key,envkey,0,KEY_SET_VALUE)
        SetValueEx(k,keyname,None,REG_SZ, value)
        FlushKey(k)
        CloseKey(k)
    else:
        pypathval = os.environ[keyname]
        valarr = [i for i in pypathval.split(";") if i!=""]
        tmparr = [i.lower() for i in valarr]
        if value.lower() not in tmparr:
            valarr.append(value)
            pypathval = ";".join(valarr)
            print pypathval
            k = OpenKey(key,envkey,0,KEY_SET_VALUE)
            SetValueEx(k,keyname,None,REG_SZ, pypathval)
            FlushKey(k)
            CloseKey(k)
        else:
            print 'already right:',pypathval

def regOSEnv(keyname,value,allorcur=1):
    if allorcur:
        key = HKEY_LOCAL_MACHINE
        envkey = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    else:
        key = HKEY_CURRENT_USER
        envkey = r"Environment"
    regkey(key,envkey,keyname,value)

if __name__=="__main__":
    thisfile = os.path.split(os.path.abspath(__file__))[0]
    parentfile = os.path.split(thisfile)[0]
    pymod = os.path.join(parentfile,'pymod')
    print pymod

    keyname = 'PYTHONPATH'
    regOSEnv(keyname, pymod)


    import sys
    pyhome = sys.prefix
    pathkey = "PATH"

    regOSEnv(pathkey,pyhome)
