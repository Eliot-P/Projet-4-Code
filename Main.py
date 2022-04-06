

from statistics import mean
from turtle import xcor
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import Code.coda_toolbox as coda
import Code.signal_processing_toolbox as sp


def squarequalitylong(x,y):
    
    long1 = np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)
    long2 = np.sqrt((x[2] - x[1])**2 + (y[2] - y[1])**2)
    long3 = np.sqrt((x[3] - x[2])**2 + (y[3] - y[2])**2)
    long4 = np.sqrt((x[0] - x[3])**2 + (y[0] - y[3])**2)
    list = [long1, long2, long3, long4]
    quality = np.std(list)
    
    return quality

def squarequalityangle(x,y):
    
    angle1 = np.arccos(((x[1] - x[0]) * (x[2] - x[1]) + (y[1] - y[0]) * (y[2] - y[1])) / (np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2) * np.sqrt((x[2] - x[1])**2 + (y[2] - y[1])**2)))
    angle2 = np.arccos(((x[2] - x[1]) * (x[3] - x[2]) + (y[2] - y[1]) * (y[3] - y[2])) / (np.sqrt((x[2] - x[1])**2 + (y[2] - y[1])**2) * np.sqrt((x[3] - x[2])**2 + (y[3] - y[2])**2)))
    angle3 = np.arccos(((x[3] - x[2]) * (x[0] - x[3]) + (y[3] - y[2]) * (y[0] - y[3])) / (np.sqrt((x[3] - x[2])**2 + (y[3] - y[2])**2) * np.sqrt((x[0] - x[3])**2 + (y[0] - y[3])**2)))
    angle4 = np.arccos(((x[0] - x[3]) * (x[1] - x[0]) + (y[0] - y[3]) * (y[1] - y[0])) / (np.sqrt((x[0] - x[3])**2 + (y[0] - y[3])**2) * np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)))
    
    list = [np.degrees(angle1), np.degrees(angle2), np.degrees(angle3), np.degrees(angle4)]
    
    quality = np.std(list)
    
    return quality

def score(x,y):
    lon = squarequalitylong(x,y)
    angle = squarequalityangle(x,y)
    return lon+angle



def find_angles_rework(xi,yi):
    m1 = np.polyfit(xi[:10],yi[:10],1)
    m2 = np.polyfit(xi[-10:],yi[-10:],1)
    theta = np.arctan((m1[0] - m2[0])/(1 + m1[0]*m2[0]))
    theta_refined = abs(theta)
    return theta_refined


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

def square_finder(f):
    time_stamps = np.linspace(0,5600,29)
    time_stamps+=f
    time_stamps = np.int_(time_stamps)
    return time_stamps

def quality_finder(time_stamps,x,y):
    qualities = np.zeros(7)
    for j in range(7):
        i = j*4
        x_coord = x[time_stamps[0+i:4+i]]
        y_coord = y[time_stamps[0+i:4+i]]
        qualities[j] = score(x_coord,y_coord)
    return qualities

def ploter(x,y,vx,vy,t,fX,fY,time_stamps,qualities):
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#bcbd22']
    plt.subplot(4,2,1)
    plt.title("x coordinates")
    for i in range(7):
        plt.axvspan(t[time_stamps[i*4]],t[time_stamps[i*4+4]],alpha=0.5,color=colors[i])
    plt.plot(t,x)
    plt.scatter(t[fX],x[fX],color='red')
    plt.scatter(t[fY],x[fY],color='green')
    plt.grid()
    
    plt.subplot(4,2,2)
    plt.title("x velocity")
    for i in range(7):
        plt.axvspan(t[time_stamps[i*4]],t[time_stamps[i*4+4]],alpha=0.5,color=colors[i])
    plt.plot(t,vx)
    plt.grid()
    plt.scatter(t[fX],vx[fX],color='red')
    plt.scatter(t[fY],vx[fY],color='green')



    plt.subplot(4,2,3)
    plt.title("y coordinates")
    for i in range(7):
        plt.axvspan(t[time_stamps[i*4]],t[time_stamps[i*4+4]],alpha=0.5,color=colors[i])
    plt.plot(t,y)
    plt.scatter(t[fX],y[fX],color='red')
    plt.scatter(t[fY],y[fY],color='green')
    plt.grid()
    
    plt.subplot(4,2,4)
    plt.title("y velocity")
    for i in range(7):
        plt.axvspan(t[time_stamps[i*4]],t[time_stamps[i*4+4]],alpha=0.5,color=colors[i])
    plt.plot(t,vy)
    plt.grid()
    plt.scatter(t[fX],vy[fX],color='red')
    plt.scatter(t[fY],vy[fY],color='green')

    plt.subplot(2,3,4)
    plt.title("trajectory")
    plt.plot(x,y)
    plt.grid()
    plt.scatter(x[fX],y[fX],color='red')
    plt.scatter(x[fY],y[fY],color='green')

    
    plt.subplot(2,3,5)
    plt.title("Recognized squares")
    for j in range(7):
        i = j * 4
        x_coord = x[time_stamps[0+i:4+i]]
        y_coord = y[time_stamps[0+i:4+i]]
        plt.scatter(x_coord,y_coord,color=colors[j])
        plt.plot([x_coord[0],x_coord[1]],[y_coord[0],y_coord[1]],color=colors[j])
        plt.plot([x_coord[1],x_coord[2]],[y_coord[1],y_coord[2]],color=colors[j])
        plt.plot([x_coord[2],x_coord[3]],[y_coord[2],y_coord[3]],color=colors[j])
        plt.plot([x_coord[3],x_coord[0]],[y_coord[3],y_coord[0]],color=colors[j])
    
    plt.subplot(2,3,6)
    plt.grid()
    plt.title('square quality')
    plt.bar(np.arange(7),qualities,color=colors)
    plt.axhline(mean(qualities))
    
    plt.show()

def data_array(df):
    x = sp.filter_signal(df["Marker5_X"])
    y = sp.filter_signal(df["Marker5_Y"])

    t = np.array(df["time"])
    vx = sp.derive(x,200)
    vy = sp.derive(y,200)
    fY = separatorVY(x,y,vx,vy,t)
    fX = separatorVX(x,y,vx,vy,t)
    return x,y,vx,vy,t,fX,fY
    
def main():
    C = coda.import_data("Data/GBIO_2022_Group_2_S1bis_20220007_009.TXT")
    x,y,vx,vy,t,fX,fY = data_array(C)
    time_stamps = square_finder(fY)
    qualities = quality_finder(time_stamps,x,y)
    ploter(x,y,vx,vy,t,fX,fY,time_stamps,qualities)

main()
