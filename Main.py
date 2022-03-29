from cmath import pi
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import Code.coda_toolbox as coda
import Code.signal_processing_toolbox as sp


def data_reader():
    header = pd.read_csv("result.csv")
    
def square_finder(x,y) : 
    dxdy = np.gradient(x,y)
    max = np.argmax(dxdy[100:])
    return dxdy,max



def find_angle(x,y) : 
    m1 = np.polyfit(x[:5],y[:5],1)[0]
    m2 = np.polyfit(x[-5:],y[-5:],1)[0]
    theta = np.arctan((m1 - m2)/(1 + m1*m2))
    theta_refined = abs(theta)
    return theta_refined

C = coda.import_data("Data/GBIO_2022_Group_2_S2_20220007_009.TXT")
#x = (C["Marker5_X"]).to_numpy()
#y = (C["Marker5_Y"]).to_numpy()
x = sp.filter_signal(C["Marker5_X"])
y = sp.filter_signal(C["Marker5_Y"])
z = sp.filter_signal(C["Marker5_Z"])
angles = []
for i in range(len(x) - 14) : 
    i+=10
    angles.append(find_angle(x[i:i+10],y[i:i+10]))
#print(angles)
f = np.argsort(-np.array(angles))[:28]
print(f)

"""
t = np.array(C["time"])
vx = np.gradient(t,x)
vy = np.gradient(t,y)
vmaxx = np.argmax(vx[40:-40])
vmaxy = np.argmax(vy)
"""
fig = plt.figure()
ax = plt.axes()
dxdy,max = square_finder(x,y)
ax.plot(x,y)
#ax.scatter(x[max],y[max],color='blue')
#ax.scatter(x[vmaxx],y[vmaxx],color='green')
ax.scatter(x[f],y[f],color='red')
plt.show()
