import pandas as pd
import csv
import os
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor as Executor
from itertools import repeat


df = pd.read_csv('AAPL.csv')


df.drop(df.columns[[1,2,3,5,6]], axis = 1, inplace = True)
df.set_index("Date", inplace = True)
list1 = []


def psigmasigma():
    a = 0
    for p in range(18, 22):
        for Usigma in range(17, 20):
            Usigma = Usigma/10
            for Dsigma in range(17, 20):
                Dsigma = Dsigma/10
                list1.append([p,Usigma,Dsigma])

psigmasigma()

def Upper_LowerBand(df, lst):
    p = f"{lst[0]}"
    Usigma = f"{lst[1]}"
    Dsigma = f"{lst[2]}"
    df['SMA'] = df.Close.rolling(window=int(f'{p}')).mean()
    df['Upper'] = df.Close.rolling(window=int(f'{p}')).std()
    df['Lower'] = df.Close.rolling(window=int(f'{p}')).std()
    df['UpperBand'] = df['SMA'] + float(Usigma)*df['Upper']
    df['LowerBand'] = df['SMA'] - float(Dsigma)*df['Lower']
    df.drop(df.columns[[3,2]], axis = 1, inplace = True)

    flag = 0
    pnl = 0
    for i in range(0, len(df)):
        if df['Close'][i] < df['LowerBand'][i] and flag == 0:
            flag = -1
        
        elif df['Close'][i] > df['LowerBand'][i] and flag == -1:
            pnl += df['Close'][i]
            flag = 0
            
        elif df['Close'][i] > df['UpperBand'][i] and flag == 0:
            flag = 1
            
        elif df['Close'][i] < df['UpperBand'][i] and flag == 1:   
            pnl -= df['Close'][i]
            flag = 0
        else:
            pass

    return print(pnl)

def multiprocessing(df, lst):

    return Upper_LowerBand(df, lst)

if __name__ == '__main__': 
    with Executor() as executor:

        results = [executor.map(multiprocessing, df, lst) for lst in list1]
      
        print(list(results))

