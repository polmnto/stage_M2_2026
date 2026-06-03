import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input") #quartet_support_dataframe
parser.add_argument("-o", "--output")
args = parser.parse_args()

df = pd.read_csv(args.input, sep = '\t')

colnames = list(df.columns)[1:]

for j in colnames:
    for i in range(df.shape[0]): #count the number of rows in the df
        values = df[j].iloc[i]
        score = values.split("|")
        if max(score) == score[0] and max(score) == score[1] or max(score) == score[0] and max(score) == score[2] or max(score) == score[1] and max(score) == score[2]:
            df.loc[i, j] = "N"
        elif max(score) == score[0]:
            df.loc[i, j] = "C"
        elif max(score) == score[1]:
            df.loc[i, j] = "D1"
        elif max(score) == score[2]:
            df.loc[i, j] = "D2"


df.to_csv(args.output, index = False, header = True, sep = '\t') 


