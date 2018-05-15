# -*- encoding:utf-8 -*-
from django.http import HttpResponse

def toList(obj):
    arr = []
    for k in obj:
        if type(k) == str:
            arr.append('"'+str(k)+'"')
        elif type(k)==unicode:
            arr.append('"'+unicode(k)+'"')
        elif type(k)==list:
            arr.append(toList(k))
        elif type(k)==dict:
            arr.append(toMap(k))
    return "["+",".join(arr)+"]" 
def toMap(obj):
    arr = []
    for k in obj:
        arr.append('"'+k+'":'+toJSON(obj[k]))
    return "{"+",".join(arr)+"}" 

def toJSON(obj):
    if type(obj)==dict:
        return toMap(obj)
    if type(obj)==list:
        return toList(obj)

def friends(request):
    friends = {"aaaa":["我","b","c"],"bbb":["a","啦啦啦"]}
    print toJSON(friends)

    return HttpResponse(toJSON(friends))

