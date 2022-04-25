from matplotlib import gridspec
import matplotlib.pyplot as plt
import numpy as np

def plotter(x,y,vx,vy,t,time_stamps,qualities,seq):
    
    mean_quality = np.mean(qualities)
    median_quality = np.median(qualities)
    std_dev = np.std(qualities)
    
    title = " Sujet : {} \n angle : {}° \n take : {} \n memorization task : {} \n success : {} \n square quality : \n   mean : {:.2f}\n   std : {:.2f}\n   median : {:.2f}"
    title = title.format(seq["subject"],seq["angle"],seq["number"],seq["memorization_task"],seq["success"],mean_quality,std_dev,median_quality)
    fig = plt.figure(figsize=[13,8])
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#bcbd22']
    
    figs = fig.subfigures(2,1)
    figs[0].text(0.025,0.8,title,va='top',ha='left',size='large')
    figs[0].suptitle("Recapitulative table of the sequence",style='oblique',size="x-large")
    
    gsA = gridspec.GridSpec(2,5,figure=figs[0])
    gsB = gridspec.GridSpec(2,5,figure=figs[1])
    ax_x = figs[0].add_subplot(gsA[0,1:3])
    ax_vx = figs[0].add_subplot(gsA[1,1:3],sharex=ax_x)
    ax_y = figs[0].add_subplot(gsA[0,3:])
    ax_vy = figs[0].add_subplot(gsA[1,3:],sharex=ax_y)
    figs[0].subplots_adjust(hspace=0,wspace=0.5,left=0.05,right=0.95)

    ax_traj = figs[1].add_subplot(gsB[:,0:2])
    ax_squares = figs[1].add_subplot(gsB[:,2:4],sharex=ax_traj,sharey=ax_traj)
    ax_quality = figs[1].add_subplot(gsB[:,4])
    figs[1].subplots_adjust(wspace=0.5,left=0.06,right=0.95)



    
    ax_x.set_title("X axis")
    ax_x.plot(t,x)
    
    ax_x.grid()
    ax_x.set_ylabel("Position [mm]")
    
    ax_vx.plot(t,vx)
    ax_vx.grid()

    ax_vx.set_xlabel("Time [s]")
    ax_vx.set_ylabel("velocity [mm/s]")



    ax_y.set_title("Y axis")
    ax_y.plot(t,y)

    ax_y.grid()
    ax_y.set_ylabel("Position [mm]")
    
    ax_vy.plot(t,vy)
    ax_vy.grid()

    ax_vy.set_xlabel("Time [s]")
    ax_vy.set_ylabel("velocity [mm/s]")

        
    ax_traj.set_title("Trajectory")
    ax_traj.set_ylabel("Y position [mm]")
    ax_traj.set_xlabel("X position [mm]")
    ax_traj.plot(x,y)
    ax_traj.grid()


    
    ax_squares.set_title("Recognized squares")
    ax_squares.set_ylabel("Y position [mm]")
    ax_squares.set_xlabel("X position [mm]")
    for j in range(7):
        i = j * 4
        x_coord = x[time_stamps[0+i:4+i]]
        y_coord = y[time_stamps[0+i:4+i]]
        ax_squares.scatter(x_coord,y_coord,color=colors[j])
        ax_traj.scatter(x_coord,y_coord,color=colors[j])
        ax_squares.plot([x_coord[0],x_coord[1]],[y_coord[0],y_coord[1]],color=colors[j])
        ax_squares.plot([x_coord[1],x_coord[2]],[y_coord[1],y_coord[2]],color=colors[j])
        ax_squares.plot([x_coord[2],x_coord[3]],[y_coord[2],y_coord[3]],color=colors[j])
        ax_squares.plot([x_coord[3],x_coord[0]],[y_coord[3],y_coord[0]],color=colors[j])
        
        ax_x.axvspan(t[time_stamps[i]],t[time_stamps[i+4]],alpha=0.5,color=colors[j])
        ax_vx.axvspan(t[time_stamps[i]],t[time_stamps[i+4]],alpha=0.5,color=colors[j])
        ax_vy.axvspan(t[time_stamps[i]],t[time_stamps[i+4]],alpha=0.5,color=colors[j])
        ax_y.axvspan(t[time_stamps[i]],t[time_stamps[i+4]],alpha=0.5,color=colors[j])
        



    
    ax_quality.grid()
    ax_quality.set_title('Square quality')
    ax_quality.bar(np.arange(7),qualities,color=colors)
    ax_quality.axhline(mean_quality)  
    
    figname = "Images/{}_{}".format(seq["subject"],seq["number"])
    
    fig.savefig(figname)