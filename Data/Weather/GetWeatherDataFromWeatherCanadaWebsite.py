# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 08:31:40 2023

Script to test env-canada python library to request:
    - current weather conditions;
    - 24-hour weather forecasts;
    - last 24-hour weather conditions.

@author: delcr
"""
###############################################################################
# LIBRAIRIES
###############################################################################
import os
import pandas as pd
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
    
    # Definitions
    Cities = ['Montreal','Quebec','Gatineau','Sherbrooke','Saguenay',
              'Trois-Rivieres']
    Past24h = ['https://weather.gc.ca/past_conditions/index_e.html?station=yul',
               'https://weather.gc.ca/past_conditions/index_e.html?station=yqb',
               'https://weather.gc.ca/past_conditions/index_e.html?station=ynd',
               'https://weather.gc.ca/past_conditions/index_e.html?station=ysc',
               'https://weather.gc.ca/past_conditions/index_e.html?station=wjo',
               'https://weather.gc.ca/past_conditions/index_e.html?station=yrq']
    Next24h = ['https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-133_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-126_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-136_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-166_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-130_metric_e.html']
    Past24h_min = []
    Past24h_mean = []
    Past24h_max = []
    Next24h_min = []
    Next24h_mean = []
    Next24h_max = []
    
    # Get data
    for i in tqdm(range(len(Past24h))):
        df_past = pd.read_html(Past24h[i])[0][['Date / Time (EDT)',
                                               'Temperature  (°C)']]
        df_future = pd.read_html(Next24h[i])[0][['Date/Time  (EDT)', 
                                                 'Temp.  (°C)']]
        df_past = df_past[df_past['Date / Time (EDT)'] != 
                          df_past['Temperature  (°C)']]
        df_future = df_future[df_future['Date/Time  (EDT)'] != 
                              df_future['Temp.  (°C)']]
        df_future['Temp.  (°C)'] = pd.to_numeric(df_future['Temp.  (°C)'],
                                                 errors='coerce') 
        df_future.dropna(inplace=True)
        
        df_past[['Temperature  (°C)','other']] = df_past['Temperature  (°C)'].\
        str.split('  ',expand=True)
        df_past['Temperature  (°C)'] = pd.to_numeric(df_past['Temperature  (°C)'],
                                                     errors='coerce') 
        df_past.dropna(inplace=True)
        
        Past24h_min.append(df_past['Temperature  (°C)'].min())
        Past24h_mean.append(df_past['Temperature  (°C)'].mean())
        Past24h_max.append(df_past['Temperature  (°C)'].max())
        Next24h_min.append(df_future['Temp.  (°C)'].min())
        Next24h_mean.append(df_future['Temp.  (°C)'].mean())
        Next24h_max.append(df_future['Temp.  (°C)'].max())
        
        pass # end of loop for i in tqdm(range(len(Past24h)))
    
    df = pd.DataFrame(data=Past24h_min,columns=['Past24h_min'],index=Cities)
    df['Past24h_mean'] = Past24h_mean
    df['Past24h_max'] = Past24h_max
    df['Next24h_min'] = Next24h_min
    df['Next24h_mean'] = Next24h_mean
    df['Next24h_max'] = Next24h_max
    
    pass # end of main program

