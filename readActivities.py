# this block initializes the structs for storing acitivities and patients

import os
from datetime import datetime
import pandas as pd
import time
from patient import Patient, Activity
import jsonpickle
import matplotlib.pyplot as plt
import plotly.express as px
import csv
import numpy as np

src = './Data/HOA_Data'
# to-do

excel = './Data/HOA_Data/chi_unix.xlsx'
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
    

#load in csvs
src = './Data/HOA_Data'
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

for patient in patients:
    local_time = patient.csv_time
    if patient is None or patient.acc is None:
        continue

    print(patient.id, local_time, local_time + len(patient.acc))
    for activity in reversed(patient.activities):
        if (activity.start + activity.length <= local_time + round(patient.acc['t'].iloc[-1])):
            samples_for_5_Seconds = 160  # 150 seconds * 32 samples/second

            # Adjust delta to start 150 seconds (in samples) earlier
            delta = int(activity.start - local_time) * 32 - samples_for_5_Seconds
            if delta < 0: delta = 0  # Ensure delta does not go negative
    
            # Adjust newlength to end 150 seconds (in samples) later
            newlength = delta + activity.length * 32 + 2 * samples_for_5_Seconds
            
            # Ensure newlength does not exceed the length of patient.acc
            if newlength > len(patient.acc):
                newlength = len(patient.acc)
            
            acc_data = patient.acc.iloc[delta:newlength]

            activity_folder_path = "Activity"
            if not os.path.exists(activity_folder_path):
                os.makedirs(activity_folder_path)  # Create the "Activity" folder if not

            # Create the directory structure
            activity_folder = os.path.join("Activity", activity.name)
            if not os.path.exists(activity_folder):
                os.makedirs(activity_folder)
            
            # Define the file path
            file_path = os.path.join(activity_folder, f"{patient.id}_{activity.name}.csv")
            
            # Save the data to a CSV file
            acc_data.to_csv(file_path)

            print(f"Saved {activity.name} data for patient {patient.id} to {file_path}")


        # #plots acceleration
        # time = patient.acc.iloc[:,3] #changed to time column
        # voltx = patient.acc.iloc[:,0]
        # volty = patient.acc.iloc[:,1]
        # voltz = patient.acc.iloc[:,2]
            
        #accplot = plt.plot(time,voltx, 'b', alpha = 0.5)
        #accplot = plt.plot(time,volty, 'r', alpha = 0.5)
        #accplot = plt.plot(time,voltz, 'g', alpha = 0.5) #trying to plot for comparison
            
        #plots derivative of acceleration    
        # derivativex = []
        # for i in range(3, len(voltx)):
        #     derivativex.append((voltx[i] - voltx[i-1])/0.03125)
        # time2 = time.drop(index = [(time.size-1), (time.size-2)])
    
        # derivativey = []
        # for i in range(3, len(volty)):
        #     derivativey.append((volty[i] - volty[i-1])/0.03125)
        # time2 = time.drop(index = [(time.size-1), (time.size-2)])

        # derivativez = []
        # for i in range(3, len(voltz)):
        #     derivativez.append((voltz[i] - voltz[i-1])/0.03125)
        # time2 = time.drop(index = [(time.size-1), (time.size-2)])

        # resultant = []
        # time3 = time2.drop(index = [(time2.size-1), (time2.size-2), (time2.size-3), (time2.size-4)]) #???
        # for i in range(3, len(derivativex)):
        #     resultant.append(np.sqrt(derivativex[i]**2 + derivativey[i]**2 + derivativez[i]**2))
        #plt.plot(time3, resultant, 'b', alpha=1)
        #plt.xlim(0, 250)
        #plt.ylim(0,500)
        #plt.show()
    

            #acc.to_csv(patient.id + activity.name + '.csv') will fill your computer with files
            
            
            #print("Local: ",activity.start - local_time, " ", activity.start  + activity.length - local_time, "Global: ", activity.start , " ", activity.start  + activity.length )
            
            #TODO
            # splice the patient.acc dataframe at the local time indices printed above, and save them into activity.acc
    print("")

