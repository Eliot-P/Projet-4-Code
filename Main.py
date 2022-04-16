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

def score(x,y):
    lon = squarequalitylong(x,y)
    angle = squarequalityangle(x,y)
    return lon+angle



def find_angles_rework(xi,yi):
    try:
        m1 = np.polyfit(xi[:10],yi[:10],1)
    except np.linalg.LinAlgError:
        return 0
    try:
        m2 = np.polyfit(xi[-10:],yi[-10:],1)
    except np.linalg.LinAlgError:
        return 0
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

def ploter(x,y,vx,vy,t,fX,fY,time_stamps,qualities,seq):
    
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
    ax_x.scatter(t[fX],x[fX],color='red')
    ax_x.scatter(t[fY],x[fY],color='green')
    ax_x.grid()
    ax_x.set_ylabel("Position [mm]")
    
    ax_vx.plot(t,vx)
    ax_vx.grid()
    ax_vx.scatter(t[fX],vx[fX],color='red')
    ax_vx.scatter(t[fY],vx[fY],color='green')
    ax_vx.set_xlabel("Time [s]")
    ax_vx.set_ylabel("velocity [mm/s]")



    ax_y.set_title("Y axis")
    ax_y.plot(t,y)
    ax_y.scatter(t[fX],y[fX],color='red')
    ax_y.scatter(t[fY],y[fY],color='green')
    ax_y.grid()
    ax_y.set_ylabel("Position [mm]")
    
    ax_vy.plot(t,vy)
    ax_vy.grid()
    ax_vy.scatter(t[fX],vy[fX],color='red')
    ax_vy.scatter(t[fY],vy[fY],color='green')
    ax_vy.set_xlabel("Time [s]")
    ax_vy.set_ylabel("velocity [mm/s]")

        
    ax_traj.set_title("Trajectory")
    ax_traj.set_ylabel("Y position [mm]")
    ax_traj.set_xlabel("X position [mm]")
    ax_traj.plot(x,y)
    ax_traj.grid()
    ax_traj.scatter(x[fX],y[fX],color='red')
    ax_traj.scatter(x[fY],y[fY],color='green')

    
    ax_squares.set_title("Recognized squares")
    ax_squares.set_ylabel("Y position [mm]")
    ax_squares.set_xlabel("X position [mm]")
    for j in range(7):
        i = j * 4
        x_coord = x[time_stamps[0+i:4+i]]
        y_coord = y[time_stamps[0+i:4+i]]
        ax_squares.scatter(x_coord,y_coord,color=colors[j])
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

def data_array(df):
    x = sp.filter_signal(df["Marker5_X"])
    y = sp.filter_signal(df["Marker5_Y"])

    t = np.array(df["time"])
    vx = sp.derive(x,200)
    vy = sp.derive(y,200)
    fY = separatorVY(x,y,vx,vy,t)
    fX = separatorVX(x,y,vx,vy,t)
    return x,y,vx,vy,t,fX,fY
    
def sequence_reader(seq):
    x,y,vx,vy,t,fX,fY = data_array(seq['dataframe'])
    time_stamps = square_finder(fY)
    qualities = quality_finder(time_stamps,x,y)
    ploter(x,y,vx,vy,t,fX,fY,time_stamps,qualities,seq)

def dataframe_maker(results):
    df = pd.read_csv(results) 
    df.columns = ['subject','angle','number','memorization_task','success']
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

def score_csv (score_seq, seq, df):
    score_moy = 0
    for i in range(7):
        score_moy+=score_seq[i]
    score_moy= score_moy/7
    for i in range(len(df)):
        seq_ref = str (df['Sujet'][i]) +","+ str(df['Position'][i]) +","+ str(df['Sequence'][i])
        if seq_ref == seq:
            df.loc[df.index[i], 'Score'] = str(score_seq)
            df.loc[df.index[i], 'Moy'] = str(score_moy) 
    df.to_csv('copy_of_' + 'result.csv')


def seq_score():
    colnames=['Sujet', 'Position', 'Sequence', 'Avec tache', 'Reussite'] 
    df = pd.read_csv('result.csv', names=colnames, na_filter=False)
    df["Score"] = ""
    df["Moy"] = ""
    for i in range(len(df)):
        seq = (df['Sujet'][i]) +","+ str(df['Position'][i]) +","+ str(df['Sequence'][i])
        #trouver la liste de score correspondant
        score_seq= [0,1,2,3,4,5,6]
        score_csv (score_seq, seq, df)
        
def add_column_markers():
    markersx = []
    markersy = []
    
    markersx.extend("Marker5_X" for i in range(55))
    markersy.extend("Marker5_Y" for i in range(55))

    markersx.extend("Marker1_X" for i in range(50))
    markersy.extend("Marker1_Y" for i in range(50))
    
    markersx.extend("Marker5_X" for i in range(2))
    markersy.extend("Marker5_Y" for i in range(2))
    
    result_marker = pd.read_csv('result.csv')
        
    result_marker['markersx'] = markersx
    result_marker['markersy'] = markersy
    
    result_marker.to_csv('result_marker.csv')
 
def mean_square_orientation():
    df = pd.read_csv("result.csv")
    subject = ['S1', 'S2', 'S3', 'S4']
    angle = ['0','90','180']
    means = [[[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0]]]
    number_with = 0
    number_without = 0
    subject_data = df['subject']
    for i in range(len(df)):
        for j in subject : 
            if str(subject_data[i])== j or str(subject_data[i])== j +'bis' :
                for k in angle : 
                    if str(df['angle'][i])== k:
                        if str(df['memorization_task'][i])=='True':
                            means[subject.index(j)][angle.index(k)][0]+= int(df['angle'][i])
                            number_with += 1
                        if str(df['memorization_task'][i])=='False':
                            means[subject.index(j)][angle.index(k)][1]+= int(df['angle'][i])
                            number_without += 1
                    else :
                        means[subject.index(j)][angle.index(k)][0] /= number_with 
                        means[subject.index(j)][angle.index(k)][1] /= number_without
                        number_with = 0
                        number_without = 0
    print(means)
    

        

        
def main():
    df = dataframe_maker('result.csv')
    sequence_reader(df.iloc[37])

warnings.simplefilter('ignore')
main()
