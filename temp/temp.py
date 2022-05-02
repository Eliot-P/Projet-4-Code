def score_csv (score_seq, score_angle, score_long, seq, df):
    score_moy = 0
    score_moy_angle = 0
    score_moy_long = 0
    for i in range(7):
        score_moy+=score_seq[i]
        score_moy_angle += score_angle[i]
        score_moy_long += score_long[i]
    score_moy= score_moy/7
    score_moy_angle /= 7
    score_moy_long/=7
    for i in range(len(df)):
        seq_ref = str (df[df.columns[0]][i]) +","+str(df[df.columns[1]][i]) +","+ str(df[df.columns[2]][i])
        if seq_ref == seq:
            df.loc[df.index[i], 'Score_global'] = str(score_seq)
            df.loc[df.index[i], 'Moy_global'] = str(score_moy) 
            df.loc[df.index[i], 'Score_long'] = str(score_long)
            df.loc[df.index[i], 'Moy_long'] = str(score_moy_long) 
            df.loc[df.index[i], 'Score_angle'] = str(score_angle)
            df.loc[df.index[i], 'Moy_angle'] = str(score_moy_angle) 
    df.to_csv('copy_of_' + 'result.csv')


def seq_score():
    df = pd.read_csv('result.csv', na_filter=False)
    
    df["Score_global"] = ""
    df["Moy_global"] = ""
    df["Score_long"] = ""
    df["Moy_long"] = ""
    df["Score_angle"] = ""
    df["Moy_angle"] = ""
    for i in range(len(df)):
        seq = (df[df.columns[0]][i]) +","+ str(df[df.columns[1]][i]) +","+ str(df[df.columns[2]][i])
        #trouver la liste de score correspondant
        score_seq= [0,1,2,3,4,5,6]
        score_angle = [0,1,2,3,4,5,6]
        score_long = [0,1,2,3,4,5,6]
        score_csv (score_seq, score_angle, score_long, seq, df)

def plot_score_global(): 
    df = pd.read_csv('copy_of_result.csv')
    angle = [0,90, 180]
    y_true_0 = 0
    y_false_0= 0
    y_true_90 = 0
    y_false_90= 0
    y_true_180 = 0
    y_false_180= 0
    mean = mean_square_orientation(df[df.columns[7]])
    for i in range (4): 

        y_true_0 +=mean[i][0][0][0]
        y_false_0 +=mean[i][0][1][0]
        y_true_90 +=mean[i][1][0][0]
        y_false_90 +=mean[i][1][1][0]
        y_true_180 +=mean[i][2][0][0]
        y_false_180 +=mean[i][2][1][0]
    y_true_0 /=4
    y_false_0/=4
    y_true_90 /=4
    y_false_90/=4
    y_true_180 /=4
    y_false_180/=4

    axe_x = np.arange(len(angle))
    plt.bar(axe_x-0.1,[y_true_0,y_true_90,y_true_180 ] , 0.2, label='with memorization')
    plt.bar(axe_x+0.1, [y_false_0,y_false_90,y_false_180 ], 0.2, label='without memorization')
    plt.xticks(axe_x, angle)
    plt.ylim((0,100))
    plt.legend()
    plt.title ("Score global des carrés en fonction de l'orientation de la chaise par pers")
    plt.xlabel("Angles d'orientation de la chaise")
    plt.ylabel("Score global des carrés (sur 100)")
    plt.show()



def plot_score_angle(): 
    df = pd.read_csv('copy_of_result.csv')
    angle = [0,90, 180]
    y_true_0 = 0
    y_false_0= 0
    y_true_90 = 0
    y_false_90= 0
    y_true_180 = 0
    y_false_180= 0
    mean = mean_square_orientation(df[df.columns[11]])
    for i in range (4): 

        y_true_0 +=mean[i][0][0][0]
        y_false_0 +=mean[i][0][1][0]
        y_true_90 +=mean[i][1][0][0]
        y_false_90 +=mean[i][1][1][0]
        y_true_180 +=mean[i][2][0][0]
        y_false_180 +=mean[i][2][1][0]
    y_true_0 /=4
    y_false_0/=4
    y_true_90 /=4
    y_false_90/=4
    y_true_180 /=4
    y_false_180/=4


    axe_x = np.arange(len(angle))
    plt.bar(axe_x-0.1,[y_true_0,y_true_90,y_true_180 ] , 0.2, label='with memorization')
    plt.bar(axe_x+0.1, [y_false_0,y_false_90,y_false_180 ], 0.2, label='without memorization')
    plt.xticks(axe_x, angle)
    plt.ylim((0,100))
    plt.legend()
    plt.title ("Score angulaire des carrés en fonction de l'orientation de la chaise par pers")
    plt.xlabel("Angles d'orientation de la chaise")
    plt.ylabel("Score angulaire des carrés (sur 100)")
    plt.show()

def plot_score_long(): 
    df = pd.read_csv('copy_of_result.csv')
    angle = [0,90, 180]
    y_true_0 = 0
    y_false_0= 0
    y_true_90 = 0
    y_false_90= 0
    y_true_180 = 0
    y_false_180= 0
    mean = mean_square_orientation(df[df.columns[9]])
    for i in range (4): 

        y_true_0 +=mean[i][0][0][0]
        y_false_0 +=mean[i][0][1][0]
        y_true_90 +=mean[i][1][0][0]
        y_false_90 +=mean[i][1][1][0]
        y_true_180 +=mean[i][2][0][0]
        y_false_180 +=mean[i][2][1][0]
    y_true_0 /=4
    y_false_0/=4
    y_true_90 /=4
    y_false_90/=4
    y_true_180 /=4
    y_false_180/=4

    axe_x = np.arange(len(angle))
    plt.bar(axe_x-0.1,[y_true_0,y_true_90,y_true_180 ] , 0.2, label='with memorization')
    plt.bar(axe_x+0.1, [y_false_0,y_false_90,y_false_180 ], 0.2, label='without memorization')
    plt.xticks(axe_x, angle)
    plt.ylim((0,100))
    plt.legend()
    plt.title ("Score des longueurs des carrés en fonction de l'orientation de la chaise par pers")
    plt.xlabel("Angles d'orientation de la chaise")
    plt.ylabel("Score des longeurs des carrés (sur 100)")
    plt.show()
    
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
    
    
def result_sequence_par_pers_par_angle(pers, persbis, angle):
    
    f = open('result.csv')
    csv_f = csv.reader(f)
    moy = 0
    
    for row in csv_f:
        if (row[0]==pers or row[0]==persbis):
            if (row[1]==str(angle) and row[3] == 'True'):
                if (row[4]=='True'):
                    moy=moy+1
    return moy       
    #print("la moyenne de réussite de "+ pers+ " pour la mémorisation est de " + str(moy) + " sur cinq pour la position "+ str(angle))
        
        
def result_sequence_par_angle(angle):
    
    f = open('result.csv')
    csv_f = csv.reader(f)
    moy = 0
    
    for row in csv_f:
        if (row[1]==str(angle) and row[3] == 'True'):
                if (row[4]=='True'):
                    moy=moy+1
    return moy/4        
    #print("la moyenne de réussite de pour la mémorisation est de " + str(moy) + " sur vingt pour la position "+ str(angle))


#def score_total(pers,persbis, angle):
    
 #   moy_sequence= result_sequence_par_pers_par_angle(pers, persbis, angle)
  #  moy_sequence_sur_dix = moy_sequence / 5
    
   # score_moy_carres = mean_sqaure_orientation_par_personne
    #score_moy_carres_sur_jspcombien = score_moy_carres /jspcombien 
    #somme = moy_sequence_sur_dix + score_moy_carres_sur_jspcombien

def analyze_length_segment(df,t): 
    x = D_E.data_array(df[df.column[6]][t])[0]
    y = D_E.data_array(df[df.column[6]][t])[1]
    fY = D_E.data_array(df[df.column[6]][t])[6]
    #longueur totale des segments x et y de chaque séquence
    seg_x = 0
    seg_y = 0
    time_stamps = D_E.square_finder(fY)
    for j in range(7): 
        i = j * 4
        x_coord = x[time_stamps[0+i:4+i]]
        y_coord = y[time_stamps[0+i:4+i]]
        seg_x += np.sqrt((x_coord[0]-x_coord[1])**2 +(y_coord[0]-y_coord[1])**2 )
        seg_y += np.sqrt((x_coord[1]-x_coord[2])**2 +(y_coord[1]-y_coord[2])**2 )
        seg_x += np.sqrt((x_coord[2]-x_coord[3])**2 +(y_coord[2]-y_coord[3])**2 )
        seg_y += np.sqrt((x_coord[3]-x_coord[0])**2 +(y_coord[3]-y_coord[0])**2 )
    #moyenne de la longueur des segments x et y de chaque séquence
    moy_x = seg_x/7
    moy_y = seg_y/7
    df.loc[df.index[t], 'Moy_x'] += moy_x
    df.loc[df.index[t], 'Moy_y'] += moy_y
    df.to_csv('verticality.csv')
        

def seq_length_segment():
    df = pd.read_csv('Dataframe_result.csv', na_filter=False)
    df["Moy_x"] = 0
    df["Moy_y"] = 0
    for i in range(len(df)):
        analyze_length_segment(df,i)


def ratio_verticality(): 
    df = pd.read_csv('verticality.csv', na_filter=False)
    moy_x_0 = 0
    moy_y_0 = 0
    moy_x_90 = 0
    moy_y_90 = 0
    moy_x_180 = 0
    moy_y_180 = 0
    for i in range(len(df)):
        if str(df[df.columns[1]][i])=='0':
            moy_x_0 += df[df.columns[7]][i]
            moy_x_0 += df[df.columns[8]][i]
        elif str(df[df.columns[1]][i])=='90':
            moy_x_90 += df[df.columns[7]][i]
            moy_x_90 += df[df.columns[8]][i]
        else :
            moy_x_180 += df[df.columns[7]][i]
            moy_x_180 += df[df.columns[8]][i]
    moy_x_0 /= 108
    moy_y_0 /= 108
    moy_x_90 /= 108
    moy_y_90 /= 108
    moy_x_180 /= 108
    moy_y_180 /= 108
    return moy_x_0/moy_y_0, moy_x_90/moy_y_90, moy_x_180/moy_y_180  

def plot_verticality(): 
    angle = [0,90, 180]
    plt.plot(['0','90','180'], ratio_verticality(), markers='o')
    plt.ylim((0,4))
    plt.title ("Rapport des longueurs moyennes sur les largeurs moyennes des carrés en fonction de l'orientation de la chaise")
    plt.xlabel("Angles d'orientation de la chaise")
    plt.ylabel("Rapport X/Y (sur 5)")
    plt.show()

def plotter_mémorization(): 
    angle = [0,90, 180]
    y=[]
    for i in range (3):   
        y.append(result_sequence_par_angle(angle[i]))
    plt.bar(['0','90','180'], y)
    plt.ylim((0,5))
    plt.title ("Moyennes des réussites de la tâche de mémorisation en fonction de l'orientation de la chaise")
    plt.xlabel("Angles d'orientation de la chaise")
    plt.ylabel("Moyenne du nombre de réussites de la tache de mémorisation (sur 5)")
    plt.show()

def plotter_mémorization_par_pers(): 
    angle = [0,90, 180]
    subject = ['S1', 'S2', 'S3', 'S4']
    y1=[]
    y2=[]
    y3=[]
    y4=[]
    for i in range (3):   
        y1.append(result_sequence_par_pers_par_angle(subject[0], subject[0]+'bis', angle[i]))
        y2.append(result_sequence_par_pers_par_angle(subject[1], subject[1]+'bis', angle[i]))
        y3.append(result_sequence_par_pers_par_angle(subject[2], subject[2]+'bis', angle[i]))
        y4.append(result_sequence_par_pers_par_angle(subject[3], subject[3]+'bis', angle[i]))
    axe_x = np.arange(len(angle))
    plt.bar(axe_x-0.15, y1, 0.1, label='S1')
    plt.bar(axe_x-0.05, y2, 0.1, label='S2')
    plt.bar(axe_x+0.05, y3, 0.1, label='S3')
    plt.bar(axe_x+0.15, y4, 0.1, label='S4')
    plt.xticks(axe_x, angle)
    plt.ylim((0,5))
    plt.legend()
    plt.title ("Réussites de la tâche de mémorisation en fonction de l'orientation de la chaise par pers")
    plt.xlabel("Angles d'orientation de la chaise")
    plt.ylabel("Nombre de réussites de la tache de mémorisation (sur 5)")
    plt.show()