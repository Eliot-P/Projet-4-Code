import Code.coda_toolbox as coda
import Code.signal_processing_toolbox as sp
import matplotlib.pyplot as plt
from Main import dataframe_maker


df = dataframe_maker("result.csv")
for i in range(107):
    iter_frame = df.iloc[i]["dataframe"]
    fig = plt.figure(figsize=[24,16])
    fig.suptitle("Entry : {}".format(i+1),size="xx-large")
    first_marker = int(iter_frame.columns[2][6]) - 1
    
    for j in range (8):
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
    fig.savefig("Images\Other\entry_{}.png".format(i+1))
    print("Finished entry {} out of 107".format(i+1))
