

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import Code.coda_toolbox as coda
import Code.signal_processing_toolbox as sp


def squarequality(x1, y1, x2, y2, x3, y3, x4, y4):
    long1 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    long2  = np.sqrt((x3 - x2)**2 + (y3 - y2)**2)
    long3 = np.sqrt((x4 - x3)**2 + (y4 - y3)**2)
    long4 = np.sqrt((x1 - x4)**2 + (y1 - y4)**2)
    
    list = [long1, long2, long3, long4]
    quality = np.std(list)
    
    return quality

def squarequalitylong(x1, y1, x2, y2, x3, y3, x4, y4):
    
    long1 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    long2 = np.sqrt((x3 - x2)**2 + (y3 - y2)**2)
    long3 = np.sqrt((x4 - x3)**2 + (y4 - y3)**2)
    long4 = np.sqrt((x1 - x4)**2 + (y1 - y4)**2)
    list = [long1, long2, long3, long4]
    qualite = np.std(list)
    
    return qualite

def squarequalityangle(x1, y1, x2, y2, x3, y3, x4, y4):
    
    angle1 = np.arccos(((x2 - x1) * (x3 - x2) + (y2 - y1) * (y3 - y2)) / (np.sqrt((x2 - x1)**2 + (y2 - y1)**2) * math.sqrt((x3 - x2)**2 + (y3 - y2)**2)))
    angle2 = np.arccos(((x3 - x2) * (x4 - x3) + (y3 - y2) * (y4 - y3)) / (np.sqrt((x3 - x2)**2 + (y3 - y2)**2) * math.sqrt((x4 - x3)**2 + (y4 - y3)**2)))
    angle3 = np.arccos(((x4 - x3) * (x1 - x4) + (y4 - y3) * (y1 - y4)) / (np.sqrt((x4 - x3)**2 + (y4 - y3)**2) * math.sqrt((x1 - x4)**2 + (y1 - y4)**2)))
    angle4 = np.arccos(((x1 - x4) * (x2 - x1) + (y1 - y4) * (y2 - y1)) / (np.sqrt((x1 - x4)**2 + (y1 - y4)**2) * math.sqrt((x2 - x1)**2 + (y2 - y1)**2)))
    
    list = [np.degrees(angle1), np.degrees(angle2), np.degrees(angle3), np.degrees(angle4)]
    
    qualite = np.std(list)
    
    return qualite

def score(x1, y1, x2, y2, x3, y3, x4, y4):
    lon = squarequalitylong(x1, y1, x2, y2, x3, y3, x4, y4)
    angle = squarequalityangle(x1, y1, x2, y2, x3, y3, x4, y4)
    if((lon == 0)  and (angle==0)):
        return 5
    elif((lon <0.5 ) and (angle<0.5)):
        return  4
    elif((lon <1 ) and (angle<1)):
        return  3
    elif((lon <3 ) and (angle<3)):
        return 2
    else:
        return 1



def find_angles_rework(xi,yi):
    m1 = np.polyfit(xi[:10],yi[:10],1)
    m2 = np.polyfit(xi[-10:],yi[-10:],1)
    theta = np.arctan((m1[0] - m2[0])/(1 + m1[0]*m2[0]))
    theta_refined = abs(theta)
    return theta_refined


C = coda.import_data("Data/GBIO_2022_Group_2_S2_20220007_005.TXT")
x = sp.filter_signal(C["Marker5_X"])
y = sp.filter_signal(C["Marker5_Y"])
z = sp.filter_signal(C["Marker5_Z"])

t = np.array(C["time"])
vx = sp.derive(x,200)
vy = sp.derive(y,200)


def separatorVY(x,y,vx,vy,t):
    vy_sample = vy[50:400]
    arg1 = np.argmin(vy_sample)
    sample_x = x[arg1:arg1+50]
    sample_y = y[arg1:arg1+50]
    angles = np.zeros_like(sample_x)
    for j in range (len(sample_x)) : 
        angles[j] = find_angles_rework(sample_x[j:j+20],sample_y[j:j+20])
    g = np.argmax(angles) + 10
    return g + arg1 + 50

def separatorVX(x,y,vx,vy,t):
    vx_sample = vx[100:400]
    arg1 = np.argmax(vx_sample)
    sample_x = x[arg1-50:arg1+200]
    sample_y = y[arg1-50:arg1+200]
    angles = np.zeros_like(sample_x)
    for j in range (len(sample_x)) : 
        angles[j] = find_angles_rework(sample_x[j:j+20],sample_y[j:j+20])
    g = np.argmax(angles) + 10
    return g + arg1 + 50


fY = separatorVY(x,y,vx,vy,t)
fX = separatorVX(x,y,vx,vy,t)

plt.subplot(4,2,1)
plt.title("x")
plt.plot(t,x)
plt.scatter(t[fX],x[fX],color='red')
plt.scatter(t[fY],x[fY],color='green')
plt.grid()
plt.subplot(4,2,2)
plt.title("vx")
plt.plot(t,vx)
plt.grid()
plt.scatter(t[fX],vx[fX],color='red')
plt.scatter(t[fY],vx[fY],color='green')


plt.subplot(4,2,3)
plt.title("y")
plt.plot(t,y)
plt.scatter(t[fX],y[fX],color='red')
plt.scatter(t[fY],y[fY],color='green')
plt.grid()
plt.subplot(4,2,4)
plt.title("vy")
plt.plot(t,vy)
plt.grid()
plt.scatter(t[fX],vy[fX],color='red')
plt.scatter(t[fY],vy[fY],color='green')

plt.subplot(2,1,2)
plt.title("traj")
plt.plot(x,y)
plt.scatter(x[fX],y[fX],color='red')
plt.scatter(x[fY],y[fY],color='green')

plt.show()

time_stamps = np.linspace(0,5600,29)
time_stamps+=fY
time_stamps = np.int_(time_stamps)

for i in range(7):
    i*=4
    plt.scatter(x[time_stamps[0+i:4+i]],y[time_stamps[0+i:4+i]])
    plt.plot(x[time_stamps[0+i:1+1+i]],y[time_stamps[0+i:1+1+i]])
    plt.plot(x[time_stamps[1+i:1+2+i]],y[time_stamps[1+i:1+2+i]])
    plt.plot(x[time_stamps[2+i:1+3+i]],y[time_stamps[2+i:1+3+i]])
    plt.plot(x[time_stamps[3+i:1+4+i]],y[time_stamps[3+i:1+4+i]])
plt.show()