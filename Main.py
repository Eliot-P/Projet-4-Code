import pandas as pd
import matplotlib.pyplot as plt

import Code.coda_toolbox as coda
import Code.signal_processing_toolbox as sigproc

def data_reader(name) :
    f = open("Data/" + name,"r")
    headers = f.readlines()[3].split('\t')
    data = pd.read_csv("Data/" + name, sep="\t", names = headers)
    data_filtered = data.drop([0,1,2,3])
    plt.plot(data_filtered["Time"].astype(float),data_filtered["Marker 09.X"].astype(float))
    plt.show()
    
    
#data_reader("test.TXT")


C = coda.import_data("Data/test.TXT")
print(C)