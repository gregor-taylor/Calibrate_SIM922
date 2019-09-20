#########################################################
#
# Script to load calibration files from diodes to
# SIM922 
#
# G Taylor - Sept 2019
#
#########################################################
from visa import *
from hardware import SIM900
import numpy as np
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from time import sleep
import csv

####SETUP####
SIM900_add = 'ASRL7'
SIM922_slot= '8'
channel_to_update = 'all' #1 to 4 or 'all'
curve_type='LINEAR'
curve_string='COOL'
#Get data curve
temp_list=[]
volt_list=[]
CalFile = askopenfilename(initialdir="Z:\\", title="Choose calibration file")
with open(CalFile) as calfile:
    calfile_reader=csv.reader(calfile, delimiter=',')
    for index, row in enumerate(calfile_reader):
        if index==0:
            pass
        else:
            temp_list.append((row[0]))
            volt_list.append((row[1]))

temp_arr=np.asarray(temp_list, dtype='float')
volt_arr=np.asarray(volt_list, dtype='float')

#SIM900 needs rounding of lakeshore values to take them
temp_arr = np.round(temp_arr, 5)
volt_arr = np.round(volt_arr, 5)
#Optional plotting to see curve
#plt.loglog(temp_arr,volt_arr )
#plt.show()

#Initialise cal
SIM900_mf=SIM900(SIM900_add)
if channel_to_update=='all':
    ch_nums=['1','2','3','4']
else:
    ch_nums=[channel_to_update]
for ch_num in ch_nums:
    SIM900_mf.write(SIM922_slot, 'CINI '+ch_num+', '+curve_type+', '+curve_string)
    sleep(1)
    #Add cal points
    #Note points must be added in increasing resistance value according to SIM921 docs
    for i in range(len(temp_list)):
        string_to_write='CAPT '+ch_num+', '+str(volt_arr[i])+', '+str(temp_arr[i])
        SIM900_mf.write(SIM922_slot, string_to_write)
        sleep(1)

    #Check the curve
    print('Calibration finished')
    print(SIM900_mf.ask(SIM922_slot, 'CINI? '+ch_num))
'''
#Option to read it back and plot it to check - reads the last one it loaded.
rb_temp=[]
rb_volt=[]
for i in range(1, len(temp_list)+1, 1):
    resp=SIM900_mf.ask(SIM922_slot, 'CAPT? '+ch_nums[-1]+', '+str(i))
    resp=resp.split(',')
    rb_volt.append(resp[0])
    rb_temp.append(resp[1])
    sleep(1)
rb_volt_arr=np.asarray(rb_volt, dtype='float')
rb_temp_arr=np.asarray(rb_temp, dtype='float')
plt.loglog(rb_temp_arr, rb_volt_arr)
plt.show()
'''
    
#Set the curve to be used
if channel_to_update=='all':
    SIM900_mf.write(SIM922_slot, 'CURV 0, USER')
else:
    SIM900_mf.write(SIM922_slot, 'CURV '+ch_num+', USER')
sleep(1)
#Check it?
print(SIM900_mf.ask(SIM922_slot, 'CURV? 0'))




