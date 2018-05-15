from geosings.core.Geom import *

import Image,ImageDraw

from Numeric import *
from geosings.core.LabelLayout import GetBetterCentroid

a = [[0,0],
     [4,0],
     [4,4],
     [0,4],
     [0,3],
     [3,3],
     [3,1],
     [0,1],
     [0,0],
        ]

textsize = (20,20)

arr = array(a)*50

geom = CreatePolygon(arr)
geom.CloseRings()

p = GetBetterCentroid(geom)
#print p
#geom2 =  geom.Intersection(p.Buffer(50))
#p = geom2.Centroid()
#geom2 =  geom.Intersection(p.Buffer(50))
#p = geom2.Centroid()
cp = p.GetX(),p.GetY()


im = Image.new('L',(300,300),100)#L
draw = ImageDraw.Draw(im)
#xys = reshape(arr, (1,-1))[0]
xys = arr.tolist()
xys = [(xy[0],xy[1]) for xy in xys]
draw.polygon(xys,fill=0)



draw.rectangle((cp[0]-2,cp[1]-2,cp[0]+2,cp[1]+2),fill=255)
im.save('a.png','PNG')
