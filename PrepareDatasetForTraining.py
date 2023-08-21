# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 09:32:05 2023

Script to prepare a complete dataset to train a model forecasting the
electricity demand difference between last and next 24 hours (24 outputs)
based on:
    - Weather (36 inputs) 
    - Beginning hour of the prediction (1 input)
    - Beginning number of day of the prediction (1 input)
    - Working days (3 inputs) - previous day, current day and next day 
    - Total number of inputs: 41

@author: delcr
"""
###############################################################################
# LIBRAIRIES
###############################################################################
import os
import pandas as pd
import numpy as np
from datetime import date
from workalendar.america.canada import Quebec
from tqdm import tqdm

###############################################################################
# FONCTIONS
###############################################################################

###############################################################################
# PROGRAMME PRINCIPAL
###############################################################################
if __name__ == "__main__":
    
    # Définir le working directory 
    cwd = os.getcwd()
    os.chdir(cwd)
    
    # Load data
    df_use = pd.read_csv('Data/ElectricityDemand/'+\
                         '2023-08-18_AllElectricityDemandData_2019_2022.csv',
                         parse_dates=['Date'])
    df_use.drop_duplicates(subset=['Date'],inplace=True)
    df_use['Date'] = df_use['Date'] - pd.Timedelta(hours=1)
    df_use.set_index('Date',drop=True,inplace=True)
    df_weather = pd.read_csv('Data/Weather/'+\
                             '2023-08-18_AllWeatherData_2019_2022.csv',
                             parse_dates=['Unnamed: 0'])
    df_weather.drop_duplicates(subset=['Unnamed: 0'],inplace=True)
    df_weather.set_index('Unnamed: 0',drop=True,inplace=True)
    
    # Merge data
    df = df_weather.merge(df_use,how='left',left_index=True,right_index=True)
    df.interpolate('linear',inplace=True)
    
    # Definitions
    ListColumns = []
    for i in ['last','next']:
        for j in ['min','mean','max']:
            for k in ['Montreal','Quebec','Gatineau','Sherbrooke','Saguenay','Trois-Rivieres']:
                ListColumns.append(i+'24h_'+j+'Temp_'+k)
                pass
            pass
        pass
    ListColumns.extend(['BeginningHour_Forecast','BeginningDay_Forecast',
                        'Workingday_Prev','Workingday_Current',
                        'Workingday_Next'])
    ListOutput = ['delta_'+str(i+1) for i in range(24)]
    ListColumns.extend(ListOutput)
    
    # Create dataset
    df_vf = pd.DataFrame()
    for i in tqdm(range(24,len(df)-25,1)):
        data=[]
        current = df.iloc[i,:]
        last24 = df.iloc[i-24:i,:]
        next24 = df.iloc[i:i+24,:]
        stat_last24= last24.agg({'Montreal': ['min', 'mean', 'max'],
                                 'Quebec': ['min', 'mean', 'max'],
                                 'Gatineau': ['min', 'mean', 'max'],
                                 'Sherbrooke': ['min', 'mean', 'max'],
                                 'Saguenay': ['min', 'mean', 'max'],
                                 'Trois-Rivieres': ['min', 'mean', 'max']})
        data.extend(stat_last24.values.flatten())
        stat_next24= next24.agg({'Montreal': ['min', 'mean', 'max'],
                                 'Quebec': ['min', 'mean', 'max'],
                                 'Gatineau': ['min', 'mean', 'max'],
                                 'Sherbrooke': ['min', 'mean', 'max'],
                                 'Saguenay': ['min', 'mean', 'max'],
                                 'Trois-Rivieres': ['min', 'mean', 'max']})
        data.extend(stat_next24.values.flatten())
        data.append(next24.index[0].hour)
        data.append(next24.index[0].weekday())
        current_day = next24.index[0]
        previous_day = next24.index[0]-pd.Timedelta(days=1)
        next_day = next24.index[0]+pd.Timedelta(days=1)
        cal = Quebec()
        data.append(int(cal.is_working_day(date(previous_day.year, 
                                                previous_day.month,
                                                previous_day.day))))
        data.append(int(cal.is_working_day(date(current_day.year, 
                                                current_day.month,
                                                current_day.day))))
        data.append(int(cal.is_working_day(date(next_day.year, 
                                                next_day.month,
                                                next_day.day))))
        diff = next24['Moyenne (MW)'].values-last24['Moyenne (MW)'].values 
        data.extend(diff.flatten())
        arrData = np.array(data).reshape((1,-1))
        df_temp = pd.DataFrame(data=arrData,columns=ListColumns)
        df_vf = pd.concat([df_vf,df_temp],ignore_index=True)
        pass # end of loop for i in tqdm(range(24,len(df)-25,1))
    
    # Save training data as csv file
    df_vf.to_csv('ProcessedTrainingDataset.csv')
    
    pass # end of main program
    
    
    
        
