#imports
import pandas as pd
import numpy as np
import scipy.stats as stats
import scipy.signal as signal


#Mean
#inputs - (x,y,z, time) data frame for one window
# outputs - mean x, meany y and mean z for window
def windowed_mean(input_df):
    input_x = np.array(input_df.lof[:, "x"])
    input_y = np.array(input_df.lof[:, "y"])
    input_z = np.array(input_df.lof[:, "z"])

    return np.mean(input_x), np.mean(input_y), np.mean(input_z)


#std dev
#inputs - (x,y,z, time) data frame for one window
# outputs - std dev x, std dev y and std dev z for window
def windowed_std_dev(input_df):
    input_x = np.array(input_df.lof[:, "x"])
    input_y = np.array(input_df.lof[:, "y"])
    input_z = np.array(input_df.lof[:, "z"])

    return np.std(input_x), np.std(input_y), np.std(input_z)

#skewness
#inputs - (x,y,z, time) data frame for one window
# outputs - skewness [x,y,z]
def windowed_skew(input_df):
    input_x = np.array(input_df.lof[:, "x"])
    input_y = np.array(input_df.lof[:, "y"])
    input_z = np.array(input_df.lof[:, "z"])

    return stats.skew(input_x), stats.skew(input_y), stats.skew(input_z)


#kurtosis
#inputs - (x,y,z, time) data frame for one window
# outputs - kurtosis [x,y,z]
def windowed_kurtosis(input_df):
    input_x = np.array(input_df.lof[:, "x"])
    input_y = np.array(input_df.lof[:, "y"])
    input_z = np.array(input_df.lof[:, "z"])

    return stats.kurtosis(input_x), stats.kurtosis(input_y), stats.kurtosis(input_z)


#zero crossing rate
#inputs - (x,y,z, time) data frame for one window
# outputs - zcr [x,y,z]
def windowed_zcr(input_df):

    def compute_zcr(input_arr):
        my_array = np.array(input_arr)
        return float(((((my_array[:-1] * my_array[1:]) < 0).sum())/len(input_arr)))

    input_x = np.array(input_df.lof[:, "x"])
    input_y = np.array(input_df.lof[:, "y"])
    input_z = np.array(input_df.lof[:, "z"])

    return compute_zcr(input_x), compute_zcr(input_y), compute_zcr(input_z)


#dominant frequency
#inputs - (x,y,z, time) data frame for one window
# outputs - pdf [x,y,z]
def df(input_df):

    def compute(input_arr):
        frequency_spectrum = np.fft.fft(input_arr)
        dom = frequency_spectrum[np.argmax(frequency_spectrum)]
        return dom
    input_x = np.array(input_df.lof[:, "x"])
    input_y = np.array(input_df.lof[:, "y"])
    input_z = np.array(input_df.lof[:, "z"])

    return compute(input_x), compute(input_y), compute(input_z)








