import pandas as pd
from matplotlib import pyplot as plt
import csv
from scipy.misc import derivative
from scipy.fft import rfft, rfftfreq
import numpy as np
import os
import scipy.fftpack
from scipy import integrate
import xlsxwriter


    
def plotData(path, idx2): #plots raw data, idx2 is first accelerometer column, should be 0
    subdata = pd.read_excel(path)
    time = subdata.iloc[:,0]
    volt1 = subdata.iloc[:,idx2]
    volt2 = subdata.iloc[:,idx2+1]
    volt3 = subdata.iloc[:,idx2+2]
    plt.plot(time,volt1)
    plt.plot(time,volt2)
    plt.plot(time,volt3)
    
    
def plotDer(path, idx2, color, scale):
    #path, column index, color, scale
    subdata = pd.read_excel(path)
    time = subdata.iloc[:,0]
    volt1 = subdata.iloc[:,idx2]
    volt2 = subdata.iloc[:,idx2+1]
    volt3 = subdata.iloc[:,idx2+2]
    
    derivativex = []
    for i in range(1, len(volt1)):
        derivativex.append((volt1[i] - volt1[i-1])/0.0125)
    time2 = time.drop((time.size-1))
    
    #plt.plot(time2, derivativex)
    #plt.show()
    #plt.savefig("seq_charts_2s/"+path+"derivative.png")
    #plt.clf()
    
    derivativey = []
    for i in range(1, len(volt2)):
        derivativey.append((volt2[i] - volt2[i-1])/0.0125)
    time2 = time.drop((time.size-1))

    #plt.plot(time2, derivativey)
    #plt.show()
    #plt.savefig("seq_charts_2s/"+path+"derivative.png")
    #plt.clf()
    
    derivativez = []
    for i in range(1, len(volt1)):
        derivativez.append((volt3[i] - volt3[i-1])/0.0125)
    time2 = time.drop((time.size-1))

    #plt.plot(time2, derivativez)
    #plt.show()
    #plt.savefig("seq_charts_2s/"+path+"derivative.png")
    #plt.clf()
    resultant = []
    time3 = time2.drop(time2.size-1)
    for i in range(1, len(derivativex)):
        resultant.append(np.sqrt(derivativex[i]**2 + derivativey[i]**2 + derivativez[i]**2))
    plt.plot(time3, resultant, color, alpha=0.5)
    plt.ylim(0, scale)
    

        
def plotFft(path, idx2, color, scale, xscale): 
    subdata = pd.read_excel(path)
    time = subdata.iloc[:,0]
    volt1 = subdata.iloc[:,idx2]
    volt2 = subdata.iloc[:,idx2+1]
    volt3 = subdata.iloc[:,idx2+2]
    
    derivativex = []
    for i in range(1, len(volt1)):
        derivativex.append((volt1[i] - volt1[i-1])/0.0125)
    time2 = time.drop((time.size-1))
    
    derivativey = []
    for i in range(1, len(volt2)):
        derivativey.append((volt2[i] - volt2[i-1])/0.0125)
    time2 = time.drop((time.size-1))
    
    derivativez = []
    for i in range(1, len(volt1)):
        derivativez.append((volt3[i] - volt3[i-1])/0.0125)
    time2 = time.drop((time.size-1))

    resultant = []
    time3 = time2.drop(time2.size-1)
    for i in range(1, len(derivativex)):
        resultant.append(np.sqrt(derivativex[i]**2 + derivativey[i]**2 + derivativez[i]**2))
    
    # Number of samplepoints
    N = len(resultant)
    # sample spacing
    T = 1.0 / 800.0
    x = np.linspace(0.0, N*T, N)
    
    #old fourier code
    #yf = scipy.fft.rfft(resultant)
    #yinteg = (2.0/N * np.abs(yf[:N//2]))
    #xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    #plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    
    #new fourier code
    xf = scipy.fft.rfftfreq(N,T)
    #makes xf scale equal to normal x scale
    xfn = [i * 5.45625 for i in xf]
    yf = scipy.fft.rfft(resultant)
    yinteg = np.abs(yf)
    plot, = plt.plot(np.abs(xfn),np.abs(yf))
   
    #plt.plot(np.abs(yf), xf, color)
    #numbers are frequency ranges, probably should be changed if needed
    PDf1 = xfn[3:6]
    essentialf2 = xfn[5:12]
    
    PDf3 = xfn[3:5]
    essentialf4 = xfn[8:12]
    enhanced = xfn[12:18]
    Norm = xfn[0:400]
    
    xtest1 = xfn[12:14]
    xtest2 = xfn[8:10]
    #trapint(xf, yf, 3, 6)
    
    integ1 = yinteg[3:6]
    integ2 = yinteg[5:12]
    integ3 = yinteg[3:5]
    integ4 = yinteg[8:12]
    integ5 = yinteg[12:18]
    normal = yinteg[0:400]
    
    
    integA = np.trapz(integ1)
    integB = np.trapz(integ2)
    integC = np.trapz(integ3)
    integD = np.trapz(integ4)
    integE = np.trapz(integ5)
    Entire = np.trapz(Norm)
    
    
    #integA = np.trapz(integ1, PDf1, T)
    #integB = np.trapz(integ2, essentialf2, T)
    #integC = np.trapz(integ3, PDf3, T)
    #integD = np.trapz(integ4, essentialf4, T)
    #Entire = np.trapz(Norm, normal, T)
    
    #integA = integrate.trapz(PDf1, integ1)
    #integB = integrate.trapz(essentialf2, integ2)
    #integC = integrate.trapz(PDf3, integ3)
    #integD = integrate.trapz(essentialf4, integ4)
    #Entire = integrate.trapz(normal, Norm)
    plt.ylim(0, scale)
    plt.xlim(0, xscale)
    #plt.axhline(y = 300, xmin = 0, xmax = 50)
    
    plt.show() 
    
    ydata = plot.get_ydata()
    xdata = plot.get_xdata()
    
    nintegA = integA/Entire
    nintegB = integB/Entire
    nintegC = integC/Entire
    nintegD = integD/Entire
    nintegE = integE/Entire
    #plt.axvline(x = 16, color = 'red')
    #print(yinteg[5], ydata[5], xdata[16], xdata[1], len(xdata))
    #print("<", test1, test2)
    #print(xfn)
    print("<", integA, integB, integC, integD, Entire, ">")
    print(nintegA, nintegB, nintegC, nintegD)
    values = [nintegA, nintegB, nintegC, nintegD]
    
    #print(values)
    with open('RTUCR.csv', mode='a', newline='') as f:
        write = csv.writer(f)
        write.writerow(values)
                                       
        
def getAll(path, idx, idx2, color1, color2, scale): #outputs all resultant graphs
    directory = path
    for filename in os.scandir(directory):
        
            filepath = filename.path
            plt.clf()
            plotDer(filepath, idx, idx2, color1, scale)
            plotDer(filepath, idx, idx2+6, color2, scale)
            plt.xlabel('Time')
            plt.ylabel('Derivative of resultant')
            plt.title(filename.path)
            plt.savefig(filename.name + ".png")
            plt.clf()
            


def allFft(path, idx, idx2, color1, scale, xscale): #outputs all relative fft values
    directory = path
    for filename in os.scandir(directory):
        filepath = filename.path
        print(filename, filepath)
        plt.clf()
        plotFft(filepath, idx, idx2, color1, scale, xscale)
        plt.xlabel('Frequency Domain')
        plt.ylabel('Amplitude')
        plt.title(filename.path)
        #plt.savefig("FFT" + filename.name + ".png")
        #with open('FFT_integrals.csv', 'w') as f:
            #write = csv.writer(f)
            #write.writerow(values)
        plt.clf()
            
            

        
        
    
        
        
    
    
    
    
        

    
    


