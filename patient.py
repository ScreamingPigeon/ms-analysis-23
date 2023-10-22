import numpy as np


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
        self.acc = acc
        self.freq = freq
        self.excel_time = excel_time

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

        df.columns = ['x (N)', 'y (N)', 'z (N)']
        df['time(s)'] = np.arange(df.shape[0])/self.freq
        self.acc = df
