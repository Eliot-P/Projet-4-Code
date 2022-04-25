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
    
    markersx.extend("Marker5_X" for i in range(55))
    markersy.extend("Marker5_Y" for i in range(55))

    markersx.extend("Marker1_X" for i in range(5))
    markersy.extend("Marker1_Y" for i in range(5))
    
    markersx.extend("Marker2_X" for i in range(9))
    markersy.extend("Marker2_Y" for i in range(9))
    
    markersx.extend("Marker1_X" for i in range(36))
    markersy.extend("Marker1_Y" for i in range(36))
    
    markersx.extend("Marker5_X" for i in range(3))
    markersy.extend("Marker5_Y" for i in range(3))
    
    result_marker = pd.read_csv('result.csv')
        
    result_marker['markersx'] = markersx
    result_marker['markersy'] = markersy
    
    result_marker.to_csv('result_marker.csv',index=False,na_rep='NaN')

    


        
def main():
    add_column_markers()
    global_df = D_E.dataframe_maker('result_marker.csv')
    global_df["Qualities_angle"] = [[] for _ in range(len(global_df))]
    global_df["Qualities_long"] = [[] for _ in range(len(global_df))]
    global_df["Qualities_added"] = [[] for _ in range(len(global_df))]
    f = open("Errors.txt","w")
    for i in range(len(global_df['number']-20)) :
        seq = global_df.iloc[i]
        
        try:
            x,y,vx,vy,t,time_stamps,qualities_added,qualities_angle,qualities_long = D_E.sequence_reader(seq)
            global_df["Qualities_angle"][i].append(qualities_angle[:])
            global_df["Qualities_long"][i].append(qualities_long[:])
            global_df["Qualities_added"][i].append(qualities_added[:])
            plotter.plotter(x,y,vx,vy,t,time_stamps,qualities_added,seq)
        except:
            global_df["Qualities_angle"][i].append(np.zeros(7)[:])
            global_df["Qualities_long"][i].append(np.zeros(7)[:])
            global_df["Qualities_added"][i].append(np.zeros(7)[:])
            f.write("An error as occured with this sequence :  subject {} take {}\n".format(global_df["subject"][i],global_df["number"][i]))
        print("finished with entry {}".format(i+1))
    f.close()
    global_df.to_csv("result_processed.csv",index=False,na_rep='NaN',columns=['subject','angle','number','memorization_task','success','markersx','markersy','Qualities_angle','Qualities_long','Qualities_added'])

warnings.simplefilter('ignore')
main()
