

import os
from datetime import datetime
import pandas as pd
import time
from patient import Patient, Activity


src = './data/HOA Data'
# to-do

excel = './data/HOA Data/chi_study_events.xlsx'
excel = pd.read_excel(excel)


activities = []
ids = []
patients = []

for i in range(len(excel)):
    row = excel.iloc[i]
    if row['Subject Index'] not in ids:
        ids.append(row['Subject Index'])

for id in ids:
    # fetch all activities for said patients
    activities = []
    for i in range(len(excel)):
        act = excel.iloc[i]
        if act['Subject Index'] == id:
            activities.append(Activity(
                act['Activity'], act['Length'], act['Record Time'], act['Subject Index']))
    patient = Patient(id, 0, activities, [None], 0)
    patients.append(patient)

print(patients[0].activities[0].name)
