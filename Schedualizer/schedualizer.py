#!/usr/bin/python

import sys
import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay
from pathlib import Path


def set_format(ind='\t'):
    dformat = input(ind + '[+] Just so we\'re clear, will you use american date format or the right one? [american/correct]: ')
    while(True):
        if(dformat=='american'):
            format = '%m/%d/%Y'
            break
        elif(dformat=='correct'):
            format = '%d/%m/%Y'
            break
        dformat = input(ind + '[+] Just try again... [american/correct]: ')
    return format

def hookie_from_file(format, ind='\t'):
    hookie_l = []
    res = ind + '[+] okay give me a filename: '
    file_n = 'n'
    while(True):
        file_n = input(res)
        if(file_n == 'n'):
            break
        hookie_p = Path("bin/hookie/" + file_n)
        if(hookie_p.is_file()):
            break
        else:
            res = ind + '\t[-] Try again?[filename/n]:'
    if(file_n != 'n'):
        hookie_f = open(hookie_p, 'r')
        try:
            lines = hookie_f.readlines()
            for l in lines:
                hookie_l.append(pd.to_datetime(l, format=format))
        except:
            print(ind + '\t[-] Bad Date format.')
            hookie_l = 'er'
    return hookie_l

print('[+] Time to Schedualize your work!')
filename = input('\t[+] Select a filename: ')
if(filename == None or filename==""):
    filename = 'time_sheet'

format = set_format(ind='\t')

hookie_l = []
res = '\t[+] Dude I have this file for days to exclude, wanna use it?[y/n]: '
while(input(res) == 'y'):
    hookie_l = hookie_from_file(format, ind='\t')
    if(hookie_l != 'er'):
        break
    res = '\t[-] Want to try again?'

if(input('\t[+] Want to instead just feed me the days you want to exclude?[y/n]: ') == 'y'):
    hookie_f = open("bin/hookie/hookie_" + filename + ".conf", 'w+')
    print('\t\t... just press enter when you\'re done')
    while(True):
        hookie_date = input('\t\t[+] Date [' + format.replace('%', '') + ']: ')
        if(hookie_date != ''):
            try:
                hookie_l.append(pd.to_datetime(hookie_date, format=format))
                hookie_f.write(hookie_date)
            except:
                print('\t\t\t[-] Bad Date format.')
        else:
            break

columns = ['date']
print('\t[+] In order, tell me which fields you need on your timesheet[name/enter]:')
print('\t\t[+] 0. date')
i = 0
while(True):
    i += 1
    field = input('\t\t[+] ' + str(i) + '. ')
    if(field == ""):
        break
    columns.append(field)

df = pd.DataFrame()
while(True):
    print(hookie_l)
    strt = input('\t\t[+] Start of activity [' + format.replace('%','') + ']: ')
    end = input('\t\t[+] End date [' + format.replace('%','') + ']: ')
    d1 = pd.to_datetime(strt, format=format)
    d2 = pd.to_datetime(end, format=format)
    tmp = pd.DataFrame(pd.date_range(d1, d2), columns=['timestamp'])
    tmp = tmp[~tmp.timestamp.isin(hookie_l)]
    tmp = tmp.set_index('timestamp')
    tmp = tmp[(tmp.index.dayofweek < 5)]
    tmp['date'] = tmp.index.strftime("%d/%m/%Y")
    #tmp['hours'] = np.where(tmp.index.dayofweek==4, "6,25", "8,75")
    for col in columns[1:]:
        tmp[col] = input('\t\t[+] ' + col + ':' )
    df = pd.concat([df, tmp])
    if(input('\t[+] Is that it?[y/n]') == 'y'):
        break
df.to_csv(filename + ".csv", sep=';', header=False, index=False)
