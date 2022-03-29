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

def find_angles_rework(xi,yi):
    m1 = np.polyfit(xi[:10],yi[:10],1)[0]
    m2 = np.polyfit(xi[-10:],yi[-10:],1)[0]
    theta = np.arctan((m1 - m2)/(1 + m1*m2))
    theta_refined = abs(theta)
    return theta_refined




def find_angle(x,y) : 
    #m1 = np.polyfit(x[:5],y[:5],1)[0]
    #m2 = np.polyfit(x[-5:],y[-5:],1)[0]
    m1 = (x[1] - x[0])/(y[1] - y[0])
    m2 = (x[3] - x[2])/(y[3] - y[2])
    theta = np.arctan((m1 - m2)/(1 + m1*m2))
    theta_refined = (theta)
    return theta_refined

C = coda.import_data("Data/GBIO_2022_Group_2_S2_20220007_008.TXT")
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
vx = sp.derive(x,200)
vy = sp.derive(y,200)

def separator(x,y,vx,vy,t):
    median = np.median(y[1000:5000])
    max = np.argmax(y)
    dist = y[max] - median
    threshold = y[max]-2*dist
    i = np.argwhere(y>threshold)[0][0]
    sample_y = y[i-50:i+10]
    sample_x = x[i-50:i+10]
    angles = np.zeros_like(sample_x)
    for j in range(len(sample_x) - 20) :
        angles[j] = find_angles_rework(sample_x[j:j+20],sample_y[j:j+20])
    f = np.argmax(-angles) +10
    return f+i-50

median = np.median(y[1000:5000])
max = np.argmax(y)
dist = y[max] - median

def animation(x,y,t):
    for i in range(len(x)) :
        if i ==0 : 
            plt.subplot(1,2,1)
            line1, =plt.plot(x[:],y[:])
            plt.subplot(2,2,2)
            line2, = plt.plot(t[:],x[:])
            plt.subplot(2,2,4)
            line3, = plt.plot(t[:],y[:])
        else:
            line1.set_data(x[:i],y[:i])
            line2.set_data(t[:i],x[:i])
            line3.set_data(t[:i],y[:i])
        plt.pause(0.0001)
    return
#animation(x,y,t)
f = separator(x,y,vx,vy,t)
plt.plot(t,y)
plt.axhline(y=median)
plt.axhline(y=y[max])
plt.axhline(y=y[max]-2*dist)
plt.scatter(t[f],y[f])
plt.grid()

plt.show()



plt.plot(x,y)
plt.scatter(x[f],y[f])
plt.show()
