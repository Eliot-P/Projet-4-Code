from cmath import pi

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
