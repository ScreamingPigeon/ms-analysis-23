import numpy as np
import json
import scipy
from scipy import signal as sig


class Activity:
    def __init__(self, name, length, start, patient_id):
        self.name = name
        self.length = length
        self.start = start
        self.patient_id = patient_id


class Patient:
    def __init__(self, id, csv_time, activities, acc, freq, excel_time):
        self.id = id
        self.csv_time = csv_time
        self.activities = activities
        self.acc = None
        self.freq = freq
        self.excel_time = 0
        self.findMinTime()

    def tldr(self):
        print('Summary for patient ' + self.id + '. ' + 'There are ' + str(len(self.acc)) + ' timestamps sampled at '+str(
            self.freq) + '. There are ' + str(len(self.activities)) + ' activites associated with this patient')

    def visualize(self):
        return self.csv_time

    def clean_acc(self, csv):
        df = csv
        self.freq = df.iloc[0][1]
        df = df.drop([0, 1])
        # processes to a magnitutde
        df = df.apply(lambda x: 9.81*(x/64), axis=0)

        df.columns = ['x', 'y', 'z']
        df['t'] = np.arange(df.shape[0])/self.freq
        self.acc = df

    def findMinTime(self):
        t = -1
        for activity in self.activities:
            if activity.start < t or t < 0:
                t = activity.start
        self.excel_time = t

    def to_json(self):
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)

    def nullify(self):
        self.id = None
        self.csv_time = None
        self.activities = None
        self.acc = None
        self.freq = None
        self.excel_time = None

    def butter(self):
        cuttoff = 7  # Hz
        data = self.acc
        b, a = sig.butter(3, cuttoff/16, btype='low', analog=False)
        x = sig.filtfilt(b, a, data['x'].to_numpy())
        y = sig.filtfilt(b, a, data['y'].to_numpy())
        z = sig.filtfilt(b, a, data['z'].to_numpy())
        return x, y, z
