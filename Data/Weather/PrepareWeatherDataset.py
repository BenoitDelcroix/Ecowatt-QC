# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 07:22:53 2023

Script to prepare the electricity demand dataset

@author: delcr
"""
###############################################################################
# LIBRAIRIES
###############################################################################
import os
import pandas as pd
from tqdm import tqdm
from datetime import date
import sys

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
    Files = ['Montreal_2019to2022.csv',
             'Quebec_2019to2022.csv',
             'Gatineau_2019to2022.csv',
             'Sherbrooke_2019to2022.csv',
             'Saguenay_2019to2022.csv',
             'Trois-Rivieres_2019to2022.csv']
    Cities = ['Montreal','Quebec','Gatineau','Sherbrooke','Saguenay',
              'Trois-Rivieres']
    
    # Process data
    df = pd.DataFrame()
    for file in tqdm(Files):
        idf = pd.read_csv(file, parse_dates=['Date/Time (LST)'])
        idf.set_index('Date/Time (LST)',inplace=True)
        idf = idf['Temp (°C)']
        df = pd.concat([df,idf],axis=1)
        pass
    df.columns = Cities
    df.interpolate('linear',inplace=True)
    df.info()
    
    # Save data as csv
    today = date.today()
    df.to_csv(str(today)+'_AllWeatherData_2019_2022.csv')
     
