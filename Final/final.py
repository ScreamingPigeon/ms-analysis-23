# this block initializes the structs for storing acitivities and patients

import os
from datetime import datetime
import pandas as pd
import time
from patient import Patient, Activity
import matplotlib.pyplot as plt
import plotly.express as px
import csv
import numpy as np

## set these!!!
os.environ['SRC'] = './Data/HOA_Data'

os.environ['EXCEL_SRC'] = './Data/HOA_Data/chi_unix.xlsx'

src = os.environ['SRC']
excel_src = os.environ['EXCEL_SRC']



# to-do

excel = excel_src
excel = pd.read_excel(excel)


activities = []
ids = []
patients = []

for i in range(len(excel)):
    row = excel.iloc[i]
    if row['Subject Index'] not in ids:
        ids.append(row['Subject Index'])

for id in ids: #flagging dupes for merging
    if len(id) >= 12:
        print(id)

temp_hold= []

for id in ids:
    # fetch all activities for each patients
    activities = []
    for i in range(len(excel)):
        act = excel.iloc[i]
        if act['Subject Index'] == id:            
            activities.append(Activity(
                act['Activity'], act['Length'], act['Record Time'], act['Subject Index']))
    patient = Patient(id, 0, activities, [None], 0, 0)
    
    if len(id) >=12:
        temp_hold.append(patient)
    else:
        patients.append(patient)




#merging temp hold with patients
for temp in temp_hold:
    found = 0
    for patient in patients:
        if patient.id in temp.id:
            patient.activities =  patient.activities + temp.activities #merge activities
            #update excel time
            patient.findMinTime()
            found =1
            break
    if (found ==0):
        temp.id = temp.id[:-1]
        print(temp.id)
        patients.append(temp)
    

csv_file = []


for path, subdirs, files in os.walk(src):
    for name in files:  # for every file in this directory
        file = os.path.join(path, name)

        if 'ACC.csv' in file:  # if file name contains acc.csv, read data
            acc = pd.read_csv(file)
            csv_file.append(acc)  # append to a list

print(len(patients), len(csv_file))



for patient in patients:
    #for every unique patient - cross reference csvs
    buffer = 3*60*60
    markers  = [0]*len(csv_file)
    for i,csv in enumerate(csv_file):
        if csv is None:
            continue
        time = float(csv.columns.values[0])
        
        if time >= (patient.excel_time - buffer) and time <= (patient.excel_time +buffer):  # within buffer
            patient.clean_acc(csv)
            markers[i]=1
            csv_file[i]=None
            i-=1
            break
    print(sum(markers), patient.id)
print(csv_file)



#print(jsonpickle.encode(patients[11], indent=4))
print('Patients without hits')

lost_patients = []
for patient in patients:
    if (patient.acc  is None):
        print(patient.id, patient.excel_time)
        lost_patients.append(patient)
print('Not found patients: ', len(lost_patients))

print('Csvs without hits')
lost_csvs = []
for csv in csv_file:
    if csv is not None:
        print(csv.head())
        lost_csvs.append(csv)
print('Not found CSVs:',  len(lost_csvs))


#second pass to match up lost_csvs with lost_patients
buffer = 2000 *60 *60
for i, csv in enumerate(lost_csvs):
    if csv is None:
        continue
    time = float(csv.columns.values[0])
    for patient in lost_patients:
        if time >= (patient.excel_time - buffer) and time <= (patient.excel_time + buffer):  # within buffer
            print('match')
            break



#### TO-DO
activity_descriptions = {
    "B1_TWT_A": "B1_TWT_A: (WALK)",
    "B1_T1": "B1_T1: (WALK)",
    "B1_TWT_B": "B1_TWT_B: (WALK)",
    "B1_T2": "B1_T2: (WALK)",
    "B2_TWT_A": "B2_TWT_A: (WALK)",
    "B2_T1": "B2_T1: (WALK)",
    "B2_TWT_B": "B2_TWT_B: (WALK)",
    "B2_T2": "B2_T2: (WALK)",
    "TWT_A Training": "TWT_A Training: (WALK)",
    "TWT_B Training": "TWT_B Training: (WALK)",
    "TM Comfortable Speed": "TM Comfortable Speed: (WALK)",
    "TMT": "trail making task: (SIT)",
    "DSST": "digit symbol task: (SIT)",
    "MoCA": "Montreal Cognitive Assessment: (SIT)",
    "HR Recovery": "HR Recovery: (STAND or SIT)",
    "Naughton Test": "Naughton Test: (WALK)",
    "SOT": "SOT: (STAND)",
    "Motor Behavioral Task": "Motor Behavioral Task: (All conditions seen here)",
    "25FW_1_T1_start": "25FW_1_T1_start: 25 foot walk, condition 1 (pre-cue), trial 1, start: (WALK)",
    "TUG_1_T2": "TUG_1_T2: timed up and go, condition 1, trial 2: (WALK)",
    "BERG1_1_T1": "BERG1_1_T1: Berg Balance Test: (see handout for order of activities)"
}

for patient in patients:
    #for patient in patients
    local_time = patient.csv_time
    if patient is None or patient.acc is None:
        continue
    
    
    print(patient.id, local_time, local_time+ len(patient.acc))

    pf = os.path.join("Final", "patient_data")
    if not os.path.exists(pf):
        os.makedirs(pf)  # Create the "Activity" folder if not
    
    # Define the file path with the modified activity name
    pf = os.path.join(pf, f"{patient.id}_ACC.csv")

    # Save the data to a CSV file
    patient.acc.to_csv(pf)
    for activity in reversed(patient.activities):
        if (activity.start+activity.length <= local_time+round(patient.acc['t'].iloc[-1])):
            # Modify the activity.name based on the mapping
            if activity.name in activity_descriptions:
                activity_name_modified = activity_descriptions[activity.name]
            else:
                activity_name_modified = activity.name  # Use original name if not found in the mapping
            
            print(activity_name_modified, "Local: ", activity.start - local_time, " ", activity.start  + activity.length - local_time, activity.length, "\n" )
            
            local_start= (activity.start - local_time)* 32 -160
            local_end = (activity.start  + activity.length - local_time)*32 +160
            if (local_start<0):
                local_start = 0
            if (local_end>len(patient.acc)-1):
                local_end = len(patient.acc)-1

            seg_act = patient.acc.iloc[int(local_start):int(local_end)]
            print(seg_act)
            
            #save stuff here
            activity_folder_path = os.path.join("Final", "Activity")
            if not os.path.exists(activity_folder_path):
                os.makedirs(activity_folder_path)  # Create the "Activity" folder if not

            # Use modified activity.name for directory and file names
            activity_folder = os.path.join(activity_folder_path, activity_name_modified)
            if not os.path.exists(activity_folder):
                os.makedirs(activity_folder)
            
            # Define the file path with the modified activity name
            file_path = os.path.join(activity_folder, f"{patient.id}_{activity_name_modified}.csv")
            
            suffix = 0

            # Check if the file exists and find a unique file name by appending a suffix
            while os.path.exists(file_path):
                suffix += 1
                file_path = f"{file_path}_{suffix}.csv"
            
            # Save the data to a CSV file
            seg_act.to_csv(file_path)

            print(f"Saved {activity_name_modified} data for patient {patient.id} to {file_path}")