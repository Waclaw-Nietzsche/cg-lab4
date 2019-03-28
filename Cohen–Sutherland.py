import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Rectangle
import numpy as np
import random

def cohensutherland(xmin, ymax, xmax, ymin, x1, y1, x2, y2):
    INSIDE, LEFT, RIGHT, LOWER, UPPER = 0, 1, 2, 4, 8

    def getclip(xa, ya):
        p = INSIDE  
        if xa < xmin:
            p |= LEFT
        elif xa > xmax:
            p |= RIGHT

        if ya < ymin:
            p |= LOWER  
        elif ya > ymax:
            p |= UPPER  
        return p

   
    k1 = getclip(x1, y1)
    k2 = getclip(x2, y2)

    while (k1 | k2) != 0:  

        if (k1 & k2) != 0: 
            return None, None, None, None

        opt = k1 or k2  
        if opt & UPPER:  
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            y = ymax
        elif opt & LOWER:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            y = ymin
        elif opt & RIGHT:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            x = xmax
        elif opt & LEFT:
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            x = xmin
        else:
            raise RuntimeError('Undefined clipping state')

        if opt == k1:
            x1, y1 = x, y
            k1 = getclip(x1, y1)
            
        elif opt == k2:
            x2, y2 = x, y
            k2 = getclip(x2, y2)
    return x1, y1, x2, y2

def newline(p1, p2):
    ax = plt.gca()
    xmin, xmax = ax.get_xbound()

    if(p2[0] == p1[0]):
        xmin = xmax = p1[0]
        ymin, ymax = ax.get_ybound()
    else:
        ymax = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmax-p1[0])
        ymin = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmin-p1[0])

    l = mlines.Line2D([xmin,xmax], [ymin,ymax])
    ax.add_line(l)
    return l

fig = plt.figure()

ax = fig.add_subplot(111)

ax.set_xlabel('X',
              fontsize = 15,    #  размер шрифта
              color = 'red',    #  цвет шрифта
)

ax.set_ylabel('Y',
              fontsize = 15,
              color = 'red',
)

amountLines = 10
lines = []

for i in range(amountLines):
    xR = np.array([random.uniform(0,10), random.uniform(0,10)])
    yR = np.array([random.uniform(0,10), random.uniform(0,10)])
    lineR = np.array([xR,yR])
    lines.append(lineR)

for i in range(amountLines):
    lineR = lines[i]
    plt.plot(lineR[0], lineR[1], marker = 'o')

for i in range(amountLines):
    lineR = lines[i]
    pointX = lineR[0]
    pointY = lineR[1]
    x1 = pointX[0]
    y1 = pointY[0]
    x2 = pointX[1]
    y2 = pointY[1]
    cx1,cy1,cx2,cy2 = cohensutherland(1,3,4,1, x1,y1,x2,y2)
    print(cx1,cy1,cx2,cy2)
    if ((cx1 != None) and (cy1 != None) and (cx2 != None) and (cy2 != None)):
        xR = np.array([cx1, cx2])
        yR = np.array([cy1, cy2])
        lineR = np.array([xR,yR])
        lines[i] = lineR
        plt.plot(lineR[0], lineR[1], c = 'r', marker = 'p')
        

x1 = np.array([-1, 7])
y1 = np.array([1, 4])
line1 = np.array([x1,y1])
plt.plot(line1[0], line1[1], marker = '_')

someX1, someY1 = 1, 1
xsize, ysize = 3, 2
someX2, someY2 = someX1 + xsize, someY1
someX3, someY3 = someX1 + xsize, someY1 + ysize
someX4, someY4 = someX1, someY1 + ysize

currentAxis = plt.gca()
currentAxis.add_patch(Rectangle((someX1, someY1), xsize, ysize, fill=None, alpha=1))

plt.show()