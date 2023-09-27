import os
import pandas as pd
import matplotlib as mp
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


'''
src - directory for source data
return - list of dataframe objects
'''
def read_data(src): 
    #to-do
    csv_file = []
    for path, subdirs, files in os.walk(src):
        for name in files: #for every file in this directory
            file = os.path.join(path, name)
            if 'ACC.csv' in file: #if file name contains acc.csv, read data
                acc = pd.read_csv(file)
                csv_file.append(acc)
    return csv_file


'''
df - dataframe of shape NxM
return - dataframe of shape (N+1)(M-1)

method removes the unix time, and sampling rate rows
Method adds column with timestamps using frequency
method renames columns for x, y and z
'''
def clean_col(df):

    frequency = df.iloc[0][1]
    df = df.drop([0, 1])
    df = df.apply(lambda x: 9.81*(x/64), axis=0) #processes to a magnitutde

    df.columns = ['x (N)', 'y (N)', 'z (N)']
    df['time(s)'] = np.arange(df.shape[0])/frequency
    return df

'''
df - dataframe to be visualized
return - plotly.express line object

Method uses Vega-Altair to render simple interactive plot of df
'''

def simple_vis(df):
    fig = px.line(df, x = 'time(s)', y = df.columns[0:3])    
    return fig


'''
dfs - list of dataframes
return plotly graph object 
'''
def many_simple(dfs):
    lines= []
    for df in dfs:
        lines.append(
            go.line(df, x = 'time(s)', y = df.columns[0:3])
        )
    

updatemenus = [
    {
        'buttons': [
            {
                'method': 'restyle',
                'label': 'Val 1',
                'args': [
                    {'y': [values_1, values_1b]},
                ]
            },
            {
                'method': 'restyle',
                'label': 'Val 2',
                'args': [
                    {'y': [values_2, values_2b]},
                ]
            }
        ],
        'direction': 'down',
        'showactive': True,
    }
]

layout = go.Layout(
    updatemenus=updatemenus,
)
