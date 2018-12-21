#!/usr/bin/python

import sys
import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay

if(len(sys.argv) != 5):
    strt = input('Start date: ')
    end = input('Start date: ')
    dformat = input('first element[day/month]: ')
    project = input('project: ')
    activity= input('activity: ')
else:
    strt = sys.argv[0]
    end = sys.argv[1]
    dformat = sys.argv[2]
    project = sys.argv[3]
    activity= sys.argv[4]

if(dformat=='month'):
    d1 = pd.to_datetime(strt, format='%m/%d/%Y')
    d2 = pd.to_datetime(end, format='%m/%d/%Y')
else:
    d1 = pd.to_datetime(strt, format='%d/%m/%Y')
    d2 = pd.to_datetime(end, format='%d/%m/%Y')

df = pd.DataFrame(pd.date_range(d1, d2), columns=['date'])
df = df.set_index('date')
df = df[df.index.dayofweek < 5]
df['datef'] = df.index.strftime("%d/%m/%Y")
df['hours'] = np.where(df.index.dayofweek==4, "6,25", "8,75")
df['project'] = project
df['activity'] = activity

filename = input("Select a filename:")
if(filename == None or filename==""):
    filename = 'hours'
    
df.to_csv(filename + ".csv", sep=';', header=False, index=False)
