def mean_square_orientation():
    df = pd.read_csv("result.csv")
    subject = np.array([['S1','S1bis'], ['S2','S2bis'], ['S3','S3bis'], ['S4','S4bis']])
    angle = ['0','90','180']
    score_S1 = [[[],[]],[[],[]],[[],[]]] #liste comprenant 3 listes représentants les 3 angles eux-même constitués de 2 listes (avec et sans mémorisation)
    score_S2 = [[[],[]],[[],[]],[[],[]]]
    score_S3 = [[[],[]],[[],[]],[[],[]]]
    score_S4 = [[[],[]],[[],[]],[[],[]]]
    score_général = [score_S1,score_S2,score_S3,score_S4]
    for i in range(len(df)): 
        position = np.where(subject==df['subject'][i])
        j = int(position[0]) #ici on récupère le numéro de la liste dans laquelle se trouve le sujet recherché (0,1,2,3)
        if str(df['memorization_task'][i])=='True':
                    score_général[j][angle.index(df['angle'][i])][0].append(int(df['Moy'][i])) #on ajoute à la liste générale[sujet][angle][avec ou sans mémo]
                
        if str(df['memorization_task'][i])=='False':
                    score_général[j][angle.index(df['angle'][i])][1].append(int(df['Moy'][i]))
    #à ce stade les 4 listes sont remplies avec les scores (=moyennes individuelles pour chaque séquence), mtn on va sortir les moyennes générales (=moyennes pour une personne et pour un angle en général (avec et sans mémo))
    moyenne_S1 = [[[],[]],[[],[]],[[],[]]]
    moyenne_S2 = [[[],[]],[[],[]],[[],[]]]
    moyenne_S3 = [[[],[]],[[],[]],[[],[]]]
    moyenne_S4 = [[[],[]],[[],[]],[[],[]]] 
    moyenne_générale = [moyenne_S1,moyenne_S2,moyenne_S3,moyenne_S4]         
    for k in range(len(score_général)):
        for l in range(len(score_général[k])):
            for m in range(len(score_général[k][l])) :
                moyenne_générale[k][l][m].append(sum(score_général[k][l][m])/len(score_général[k][l][m]))  
    #taadaaaa toutes les moyennes sont faites        
