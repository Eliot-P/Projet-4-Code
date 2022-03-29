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

def data_reader():
    header = pd.read_csv("result.csv")
    
def square_finder(x,y) : 
    dxdy = np.gradient(x,y)
    max = np.argmax(dxdy[100:])
    return dxdy,max

def find_angles_rework(x,y):
    m1 = np.polyfit(x[:50],y[:50],1)[0]
    m2 = np.polyfit(x[-50:],y[-50:],1)[0]
    theta = np.arctan((m1 - m2)/(1 + m1*m2))
    theta_refined = abs(theta)
    return theta_refined




def find_angle(x,y) : 
    #m1 = np.polyfit(x[:5],y[:5],1)[0]
    #m2 = np.polyfit(x[-5:],y[-5:],1)[0]
    m1 = (x[1] - x[0])/(y[1] - y[0])
    m2 = (x[3] - x[2])/(y[3] - y[2])
    theta = np.arctan((m1 - m2)/(1 + m1*m2))
    theta_refined = abs(theta)
    return theta_refined

C = coda.import_data("Data/GBIO_2022_Group_2_S2_20220007_009.TXT")
#x = (C["Marker5_X"]).to_numpy()
#y = (C["Marker5_Y"]).to_numpy()
x = sp.filter_signal(C["Marker5_X"])
y = sp.filter_signal(C["Marker5_Y"])
z = sp.filter_signal(C["Marker5_Z"])
angles = np.zeros(len(x))
"""
for i in range(len(x) - 100) : 
    
    angles[i+50] = (find_angles_rework(x[i:i+100],y[i:i+100]))
#print(angles)
f = np.argsort(-np.array(angles))[:28]
#print(f)
"""

t = np.array(C["time"])
vx = sp.derive(sp.derive(x,200),200)
vy = np.gradient(t,y)
vmaxx = np.argmax(vx[40:-40])
vmaxy = np.argmax(vy)

fig = plt.figure()
ax = plt.axes()
dxdy,max = square_finder(x,y)

fig.subplot(2,1,1)
ax.plot(t,x)
ax.grid()
fig.subplot(2,1,2)
ax.plot(t,vx)
ax.grid()
#ax.set_ylim(-50,50)
#ax.scatter(x[max],y[max],color='blue')
#ax.scatter(x[vmaxx],y[vmaxx],color='green')
#ax.scatter(x[f],y[f],color='red')
plt.show()
