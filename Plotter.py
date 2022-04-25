from matplotlib import gridspec
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

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
    
    figname = "Images/Out/{}_{}".format(seq["subject"],seq["number"])
    
    fig.savefig(figname)
    
def sequence_quality_plotter(df):
    
    ax = sns.catplot(y="qualiti_long",x="renumber",hue="memorization_task",data=df,col="subject",row="angle",kind="box",palette="Set3")
    plt.savefig("Images/General_qualities_long.png")
    plt.clf()
    
    ax = sns.catplot(y="qualiti_angle",x="renumber",hue="memorization_task",data=df,col="subject",row="angle",kind="box",palette="Set3")
    plt.savefig("Images/General_qualities_angle.png")
    plt.clf()
    
    ax = sns.catplot(y="qualiti_added",x="renumber",hue="memorization_task",data=df,col="subject",row="angle",kind="box",palette="Set3")
    plt.savefig("Images/General_qualities_added.png")
    plt.clf()
    
    ax=sns.catplot(x="renumber",y="qualiti_added",hue="memorization_task",data=df,col="angle",palette="Set3",kind="box")
    plt.savefig("Images/Mean_qualities_added.png")
    plt.clf()
    
    ax=sns.catplot(x="renumber",y="qualiti_angle",hue="memorization_task",data=df,col="angle",palette="Set3",kind="box")
    plt.savefig("Images/Mean_qualities_angle.png")
    plt.clf()
    
    ax=sns.catplot(x="renumber",y="qualiti_long",hue="memorization_task",data=df,col="angle",palette="Set3",kind="box")
    plt.savefig("Images/Mean_qualities_long.png")
    plt.clf()
    
def memorization(df):
    data = df[(df["memorization_task"] == True) &(df["success"]==True)]
    axn = sns.countplot(x="angle",hue="subject",data=data,palette="Set3")
    plt.savefig("Images/memorization.png")
    plt.clf()
    
def DTC_calculator(df):
    S1_0_No_memo = df[(df['subject']==1) & (df['angle']==0) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S1_0_memo = df[(df['subject']==1) & (df['angle']==0) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S1_0_DTC = ((S1_0_memo - S1_0_No_memo)/S1_0_No_memo*100)
    
    S1_90_No_memo = df[(df['subject']==1) & (df['angle']==90) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S1_90_memo = df[(df['subject']==1) & (df['angle']==90) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S1_90_DTC = ((S1_90_memo - S1_90_No_memo)/S1_90_No_memo*100)
    
    S1_180_No_memo = df[(df['subject']==1) & (df['angle']==180) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S1_180_memo = df[(df['subject']==1) & (df['angle']==180) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S1_180_DTC = ((S1_180_memo - S1_180_No_memo)/S1_180_No_memo*100)
    
    S2_0_No_memo = df[(df['subject']==2) & (df['angle']==0) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S2_0_memo = df[(df['subject']==2) & (df['angle']==0) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S2_0_DTC = ((S2_0_memo - S1_0_No_memo)/S2_0_No_memo*100)
    
    S2_90_No_memo = df[(df['subject']==2) & (df['angle']==90) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S2_90_memo = df[(df['subject']==2) & (df['angle']==90) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S2_90_DTC = ((S2_90_memo - S2_90_No_memo)/S2_90_No_memo*100)
    
    S2_180_No_memo = df[(df['subject']==2) & (df['angle']==180) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S2_180_memo = df[(df['subject']==2) & (df['angle']==180) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S2_180_DTC = ((S2_180_memo - S2_180_No_memo)/S2_180_No_memo*100)
    
    S3_0_No_memo = df[(df['subject']==3) & (df['angle']==0) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S3_0_memo = df[(df['subject']==3) & (df['angle']==0) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S3_0_DTC = ((S3_0_memo - S3_0_No_memo)/S3_0_No_memo*100)
    
    S3_90_No_memo = df[(df['subject']==3) & (df['angle']==90) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S3_90_memo = df[(df['subject']==3) & (df['angle']==90) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S3_90_DTC = ((S3_90_memo - S3_90_No_memo)/S3_90_No_memo*100)
    
    S3_180_No_memo = df[(df['subject']==3) & (df['angle']==180) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S3_180_memo = df[(df['subject']==3) & (df['angle']==180) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S3_180_DTC = ((S3_180_memo - S3_180_No_memo)/S3_180_No_memo*100)
    
    S4_0_No_memo = df[(df['subject']==4) & (df['angle']==0) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S4_0_memo = df[(df['subject']==4) & (df['angle']==0) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S4_0_DTC = ((S4_0_memo - S4_0_No_memo)/S4_0_No_memo*100)
    
    S4_180_No_memo = df[(df['subject']==4) & (df['angle']==180) & (df['memorization_task'] == False)]['qualiti_added'].mean()
    S4_180_memo = df[(df['subject']==4) & (df['angle']==180) & (df['memorization_task'] == True)]['qualiti_added'].mean()
    S4_180_DTC = ((S4_180_memo - S4_180_No_memo)/S4_180_No_memo*100)
    
    
    dic = {'subject': [1,1,1,2,2,2,3,3,3,4,4],'angle':[0,90,180,0,90,180,0,90,180,0,180],'DTC':[S1_0_DTC,S1_90_DTC,S1_180_DTC,S2_0_DTC,S2_90_DTC,S2_180_DTC,S3_0_DTC,S3_90_DTC,S3_180_DTC,S4_0_DTC,S4_180_DTC]}
    frame = pd.DataFrame(data=dic)
    ax = sns.barplot(x='subject',y='DTC',hue='angle',data=frame,palette="Set3")
    plt.savefig("Images\Dual_task_cost.png")
    plt.clf()
