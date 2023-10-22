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
            acc = pd.read_csv(file)
            csv_file.append(acc)  # append to a list

for i in range(len(excel)):  # for every row in the excel
    subject = excel.iloc[i]
    excel.at[i, 'Record Time'] = time.mktime(
        subject['Record Time'].timetuple())  # converted to unix timetamping

excel.to_excel(excel_writer='./data/HOA Data/chi_unix.xlsx',
               sheet_name='chi_unix.xlsx')  # export as excel for visual inspection

correlate = []  # contains pair of csv file affiliated with excel row entries


print(len(csv_file), 'number of records')  # total number of csvs


for csv in csv_file:  # for each csv
    csv_record = float(csv.columns.values[0])  # get the time
    # cross reference record timestamps to the
    offset = 4 * 60 * 60  # create offset

    # search excel rows for time which is within margin of error set by offset
    hit = excel.loc[(excel['Record Time'] <= csv_record + offset)
                    & (excel['Record Time'] >= csv_record - offset)]
    if len(hit) == 0:  # if no matches, ping terminal
        print('Could not find hit for')
        # print the record time of the csv file which could not be found, useful during visual inspection
        print(csv_record)
        continue  # skip last statement
    correlate.append([csv, hit])  # if matches, append to correlate list

sum = 0  # keep track of number of hits in excel

for item in correlate:  # for ever pairwise correlation
    source = item[0]  # csv
    hits = item[1]  # list of excel hits
    print(source.head())  # print head of csv
    sum += len(hits)  # count number of hits
    print(len(hits), 'hits')
    print(hits.head(50))
    print()


print('Total excel hits =', sum, '/', len(excel))
print('Total csv hits =', len(correlate), '/', len(csv_file))
