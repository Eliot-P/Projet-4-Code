from matplotlib import gridspec
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings

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

def quality_ratio(x,y):
    ysorted = y.argsort()

    up1 = ysorted[0]
    up2 = ysorted[1]
    down1 = ysorted[3]
    down2 = ysorted[2]
    
    top = np.sqrt((x[up1] - x[up2])**2 + (y[up1] - y[up2])**2)
    bottom = np.sqrt((x[down1] - x[down2])**2 + (y[down1] - y[down2])**2)
    
    xsorted=x.argsort()
    right1 = xsorted[0]
    right2 = xsorted[1]
    left1 = xsorted[3]
    left2 = xsorted[2]
    right = np.sqrt((x[right1] - x[right2])**2 + (y[right1] - y[right2])**2)
    left = np.sqrt((x[left1] - x[left2])**2 + (y[left1] - y[left2])**2)
    
    ratio = (top+bottom)/(right+left)
    
    return ratio

def quality_finder(time_stamps,x,y):
    qualities_angle = np.zeros(7)
    qualities_long= np.zeros(7)
    qualities_ratio = np.zeros(7)
    for j in range(7):
        i = j*4
        x_coord = x[time_stamps[0+i:4+i]]
        y_coord = y[time_stamps[0+i:4+i]]
        qualities_angle[j] = squarequalityangle(x_coord,y_coord)
        qualities_long[j] = squarequalitylong(x_coord,y_coord)
        qualities_ratio[j] = quality_ratio(x_coord,y_coord)
    return qualities_angle, qualities_long, qualities_ratio

def separator_rework(x,y,vx,vy,t):
    v= np.sqrt(vx*vx+vy*vy)
    max = np.nanmax(v)
    indexes = np.argwhere((v<0.10*max))
    indexes_refined = []
    for i in range(1,len(indexes)-1):
        if indexes[i+1,0] - indexes[i,0] > 50:
            indexes_refined.append(indexes[i,0])
        if indexes[i,0] - indexes[i-1,0] > 50 :
            indexes_refined.append(indexes[i,0])
    
    indexes_refined = indexes_refined[1:57]
    stamps = np.zeros(29,dtype=int)
    j=0
    for i in range(0,len(indexes_refined),2):
        start = indexes_refined[i]
        stop  = indexes_refined[i+1]
        stamps[j] = (np.argmin(v[start:stop+1]) + start)
        j+=1
        
    stamps[-1] = stamps[-2] + 200
    return(stamps)

def data_array(seq):
    df = seq["dataframe"]
    x = sp.filter_signal(df[seq["markersx"]].interpolate(method='spline',order=3,s=0.))
    y = sp.filter_signal(df[seq["markersy"]].interpolate(method='spline',order=3,s=0.))

    t = np.array(df["time"])
    vx = sp.derive(x,200)
    vy = sp.derive(y,200)

    return x,y,vx,vy,t
    
def sequence_reader(seq):
    x,y,vx,vy,t = data_array(seq)
    time_stamps = separator_rework(x,y,vx,vy,t)
    qualities_angle, qualities_long, qualities_ratio = quality_finder(time_stamps,x,y)
    return x,y,vx,vy,t,time_stamps,qualities_ratio,qualities_angle,qualities_long

def dataframe_maker(results):
    df = pd.read_csv(results) 
    df.columns = ['subject','angle','number','memorization_task','success','markersx','markersy']
    subject_data = df['subject']
    number_data = df['number']
    liste_data = []
    
    for i in range(len(subject_data)) :
        if len(str(number_data[i])) == 1:
            liste_data.append(coda.import_data('Data/GBIO_2022_Group_2_'+str(subject_data[i])+'_20220007_00'+str(number_data[i])+'.TXT'))
        else : 
            liste_data.append(coda.import_data('Data/GBIO_2022_Group_2_'+str(subject_data[i])+'_20220007_0'+str(number_data[i])+'.TXT'))
    
    df.insert(5,'dataframe',liste_data)
    return df

    