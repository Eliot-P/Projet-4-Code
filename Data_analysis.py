import numpy as np
import pandas as pd
from statsmodels.stats.anova import AnovaRM

def anova_analysis(df):
    f = open('Anova_out.txt','w')
    anova_ratio = AnovaRM(data=df,depvar='quality_ratio',subject='subject',within=['memorization_task','angle'],aggregate_func='mean')
    ratio_result = str(anova_ratio.fit())
    f.write("Anova with quality criterion : ratio\n")
    f.write(ratio_result + "\n")
    anova_long = AnovaRM(data=df,depvar='quality_long',subject='subject',within=['memorization_task','angle'],aggregate_func='mean')
    long_result = str(anova_long.fit())
    f.write("Anova with quality criterion : std dev of lenght\n")
    f.write(long_result + "\n")
    anova_angles = AnovaRM(data=df,depvar='quality_angle',subject='subject',within=['memorization_task','angle'],aggregate_func='mean')
    angles_result = str(anova_angles.fit())
    f.write("Anova with quality criterion : std dev of angles\n")
    f.write(angles_result + "\n")
    f.close()
    return

def main():
    df = pd.read_csv("result_processed.csv")
    frame_argument = df[(df["subject"]!=4)]
    anova_analysis(frame_argument)
    return

main()