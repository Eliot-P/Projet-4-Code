from cmath import pi

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import Code.coda_toolbox as coda
import Code.signal_processing_toolbox as sp

df = pd.read_csv("result.csv") 
df.columns = ['sujet','angle','numéro','séquence','réussite']
C = coda.import_data("Data/GBIO_2022_Group_2_S2_20220007_009.TXT")
sujet_data = df['sujet']
numéro_data = df['numéro']
liste_data = []

for i in range(len(sujet_data)) :
    if len(str(numéro_data[i])) == 1:
        liste_data.append(coda.import_data('Data/GBIO_2022_Group_2_'+str(sujet_data[i])+'_20220007_00'+str(numéro_data[i])+'.TXT'))
    else : 
        liste_data.append(coda.import_data('Data/GBIO_2022_Group_2_'+str(sujet_data[i])+'_20220007_0'+str(numéro_data[i])+'.TXT'))
   
df.insert(5,'dataframe',liste_data)
print(df)
