import Code.coda_toolbox as coda
import Code.signal_processing_toolbox as sp
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import Data_extraction as D_E
import warnings
import Main as M


def markers_ploter(df):
    
    h = 8
    for i in range(108):
        if i == 105 : 
            h-=1
        frame = df.iloc[i]
        iter_frame=frame["dataframe"]
        fig = plt.figure(figsize=[24,16])
        fig.suptitle("Subject : {} --- take : {}".format(frame["subject"],frame["number"]),size="xx-large")

        for j in range (h):
            ax_em = fig.add_subplot(4,8,j*4+1)
            ax_xy = fig.add_subplot(4,8,j*4+2)
            ax_xz = fig.add_subplot(4,8,j*4+3)
            ax_yz = fig.add_subplot(4,8,j*4+4)
            
            
            ax_xy.set_title("x y")
            ax_xz.set_title("x z")
            ax_yz.set_title("y z")

            x = (iter_frame.iloc[:,(j*4)+1])
            y = (iter_frame.iloc[:,(j*4)+2])
            z = (iter_frame.iloc[:,(j*4)+3])

            ax_xy.plot(x,y)
            ax_xz.plot(x,z)
            ax_yz.plot(y,z)
            
            
            ax_em.text(0.2,0.5,iter_frame.columns[(j*4)+1][:-2])
        fig.subplots_adjust(wspace=0.5,hspace=0.5)
        fig.savefig("Images\Other\{}_{}_{}.png".format(i+1,frame["subject"],frame["number"]))
        print("Finished entry {} out of 108".format(i+1))
    return 

def position_speed_plotter(x,xnew,y,ynew,vx,vxnew,vy,vynew,t,seq,i):
    
    
    title = " Sujet : {} \n angle : {}° \n take : {} \n memorization task : {} \n success : {} \n marker X : {}\n marker Y : {}"
    title = title.format(seq["subject"],seq["angle"],seq["number"],seq["memorization_task"],seq["success"],seq["markersx"],seq["markersy"])
    fig = plt.figure(figsize=[13,8])
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#bcbd22']
    
    figs = fig.subfigures(2,1)
    figs[0].text(0.025,0.8,title,va='top',ha='left',size='large')
    figs[0].suptitle("Interpolation recapitulative table",style='oblique',size="x-large")
    
    gsA = gridspec.GridSpec(2,5,figure=figs[0])
    gsB = gridspec.GridSpec(2,5,figure=figs[1])
    ax_x = figs[0].add_subplot(gsA[0,1:3])
    ax_vx = figs[0].add_subplot(gsA[1,1:3],sharex=ax_x)
    ax_y = figs[0].add_subplot(gsA[0,3:])
    ax_vy = figs[0].add_subplot(gsA[1,3:],sharex=ax_y)
    figs[0].subplots_adjust(hspace=0,wspace=0.5,left=0.05,right=0.95)

    ax_traj = figs[1].add_subplot(gsB[:,0:2])
    ax_squares = figs[1].add_subplot(gsB[:,2:4])
    figs[1].subplots_adjust(wspace=0.5,left=0.06,right=0.95)



    
    ax_x.set_title("X axis")
    ax_x.plot(t,xnew,color='red')
    ax_x.plot(t,x,color='blue')
    ax_x.grid()
    ax_x.set_ylabel("Position [mm]")
    
    ax_vx.plot(t,vxnew,color='red')
    ax_vx.plot(t,vx,color='blue')
    ax_vx.grid()
    ax_vx.set_xlabel("Time [s]")
    ax_vx.set_ylabel("velocity [mm/s]")



    ax_y.set_title("Y axis")
    ax_y.plot(t,ynew,color='red')
    ax_y.plot(t,y,color='blue')
    ax_y.grid()
    ax_y.set_ylabel("Position [mm]")
    
    ax_vy.plot(t,vynew,color='red')
    ax_vy.plot(t,vy,color='blue')
    ax_vy.grid()
    ax_vy.set_xlabel("Time [s]")
    ax_vy.set_ylabel("velocity [mm/s]")

        
    ax_traj.set_title("Trajectory")
    ax_traj.set_ylabel("Y position [mm]")
    ax_traj.set_xlabel("X position [mm]")
    ax_traj.plot(x,y)
    ax_traj.grid()


    
    ax_squares.set_title("Interpolated trajectory")
    ax_squares.set_ylabel("Y position [mm]")
    ax_squares.set_xlabel("X position [mm]")
    ax_squares.plot(xnew,ynew)

    
    figname = "Images/In/{}_{}_{}.png".format(i+1,seq["subject"],seq["number"])
    
    fig.savefig(figname)
    return


def data_array_new(seq,i):
    order = 3
    l1 = [25,27,29,30,43,44,45,46,48,50,55,56]
    if i in l1:
        order = 1
        
    df = seq["dataframe"]
    x = sp.filter_signal(df[seq["markersx"]])
    y = sp.filter_signal(df[seq["markersy"]])

    t = np.array(df["time"])
    vx = sp.derive(x,200)
    vy = sp.derive(y,200)
    
    x_new=sp.filter_signal(df[seq["markersx"]].interpolate(method='spline',order=order,s=0.))
    y_new=sp.filter_signal(df[seq["markersy"]].interpolate(method='spline',order=order,s=0.))
    
    vx_new = sp.derive(x_new,200)
    vy_new = sp.derive(y_new,200)

    return x,y,vx,vy,t,x_new,y_new,vx_new,vy_new
    

def position_speed_iterator(df):
    for i in range(108):
        seq = df.iloc[i]
        x,y,vx,vy,t,x_new,y_new,vx_new,vy_new=data_array_new(seq,i+1)        
        position_speed_plotter(x,x_new,y,y_new,vx,vx_new,vy,vy_new,t,seq,i)
        print("Data tester : finished entry {}".format(i+1))
        
def main():
    df = D_E.dataframe_maker('result_marker.csv')
    position_speed_iterator(df)
    
warnings.simplefilter('ignore')
M.add_column_markers()
main()
