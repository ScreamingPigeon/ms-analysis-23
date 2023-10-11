import os
from datetime import datetime
import pandas as pd
import time
src = './data/HOA Data'
    # to-do

excel = './data/HOA Data/chi_study_events.xlsx'
excel = pd.read_excel(excel)
csv_file = []
for path, subdirs, files in os.walk(src):
    for name in files:  # for every file in this directory
        file = os.path.join(path, name)
        if 'ACC.csv' in file:  # if file name contains acc.csv, read data
            print(path[-13:])
            acc = pd.read_csv(file)

            csv_file.append(acc)

for i in range(len(excel)):
    subject = excel.iloc[i]
    
    print(time.mktime(subject['Record Time'].timetuple()))
