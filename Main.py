from matplotlib import gridspec
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings

import Code.coda_toolbox as coda
import Code.signal_processing_toolbox as sp

import Plotter as plotter
import Data_extraction as D_E


def add_column_markers():
    markersx = []
    markersy = []
    
    markersx.extend("Marker5_X" for i in range(6))
    markersy.extend("Marker5_Y" for i in range(6))
    
    markersx.extend("Marker6_X" for i in range(24))
    markersy.extend("Marker6_Y" for i in range(24))

    markersx.extend("Marker5_X" for i in range(10))
    markersy.extend("Marker5_Y" for i in range(10))
    
    markersx.extend("Marker6_X" for i in range(1))
    markersy.extend("Marker6_Y" for i in range(1))
    
    markersx.extend("Marker5_X" for i in range(11))
    markersy.extend("Marker5_Y" for i in range(11))
    
    markersx.extend("Marker6_X" for i in range(2))
    markersy.extend("Marker6_Y" for i in range(2))
    
    markersx.extend("Marker5_X" for i in range(1))
    markersy.extend("Marker5_Y" for i in range(1))
    
    markersx.extend("Marker1_X" for i in range(1))
    markersy.extend("Marker1_Y" for i in range(1))
    
    markersx.extend("Marker2_X" for i in range(1))
    markersy.extend("Marker2_Y" for i in range(1))
    
    markersx.extend("Marker1_X" for i in range(1))
    markersy.extend("Marker1_Y" for i in range(1))
    
    markersx.extend("Marker2_X" for i in range(11))
    markersy.extend("Marker2_Y" for i in range(11))
    
    markersx.extend("Marker1_X" for i in range(10))
    markersy.extend("Marker1_Y" for i in range(10))
    
    markersx.extend("Marker2_X" for i in range(9))
    markersy.extend("Marker2_Y" for i in range(9))

    markersx.extend("Marker1_X" for i in range(17))
    markersy.extend("Marker1_Y" for i in range(17))

    markersx.extend("Marker5_X" for i in range(3))
    markersy.extend("Marker5_Y" for i in range(3))
    
    result_marker = pd.read_csv('result.csv')
        
    result_marker['markersx'] = markersx
    result_marker['markersy'] = markersy
    
    result_marker.to_csv('result_marker.csv',index=False,na_rep='NaN')

    


        
def main():
    add_column_markers()
    global_df = D_E.dataframe_maker('result_marker.csv')
    
    f = open("Errors.txt","w")
    data_list = []
    S1_0 = [1,1,2,2,3,3,4,4,5,5]
    S1_90 = [1,1,2,2,3,3,4,4,5,5]
    S1_180 = [1,1,2,2,3,3,4,4,5,5]
    S2_0 = [1,1,2,2,3,3,4,4,5,5]
    S2_90 = [1,1,2,2,3,3,4,4,5,5]
    S2_180 = [1,1,2,2,3,3,4,4,5,5]
    S3_0 = [1,1,2,2,3,3,4,4,5]
    S3_90 = [1,1,2,2,3,3,4,4,5,5]
    S3_180 = [1,1,2,2,3,3,4,4,5]
    S4_0 = [1,1,2,2,3,3,4,4,5,5]
    S4_180 = [1,1,2,2,3,3,4,4,5,5]
    renumbering = [*S1_0,*S1_90,*S1_180,*S2_0,*S2_90,*S2_180,*S3_0,*S3_90,*S3_180,*S4_0,*S4_180]
    len(renumbering)
    for i in range(108) :
        seq = global_df.iloc[i]
        if seq['subject'] == "S1" :
            s = 1
        if seq['subject'] == "S1bis":
            s= 1
        if seq['subject'] == "S2":
            s = 2
        if seq['subject'] == "S3":
            s = 3
        if seq['subject'] == "S3bis":
            s= 3
        if seq['subject'] == "S4":
            s = 4

        try:
            x,y,vx,vy,t,time_stamps,qualities_ratio,qualities_angle,qualities_long = D_E.sequence_reader(seq)
            for j in range(7):
                data_list.append([s,seq['angle'],seq['number'],seq['memorization_task'],seq['success'],qualities_angle[j],qualities_long[j],qualities_ratio[j],renumbering[i]])
                
            plotter.plotter(x,y,vx,vy,t,time_stamps,qualities_ratio,seq)
        except:
            for j in range(7):
                data_list.append([s,seq['angle'],seq['number'],seq['memorization_task'],seq['success'],np.nan,np.nan,np.nan,renumbering[i]])
            f.write("An error as occured with this sequence entry:{}  subject {} take {} with marker {}\n".format(i+1,global_df["subject"][i],global_df["number"][i],global_df["markersx"][i]))
        print("finished with entry {}".format(i+1))
    result_df = pd.DataFrame(data_list,columns=['subject','angle','number','memorization_task','success','quality_angle','quality_long','quality_ratio','renumber'])
    f.close()
    
    
    result_df.to_csv("result_processed.csv",index=False,na_rep='NaN')
    
    
warnings.simplefilter('ignore')
#main()

def result_reader():
    global_df = pd.read_csv("result_processed.csv")
    plotter.sequence_quality_plotter(global_df)
    plotter.memorization(global_df)
    plotter.DTC_calculator(global_df)

result_reader()