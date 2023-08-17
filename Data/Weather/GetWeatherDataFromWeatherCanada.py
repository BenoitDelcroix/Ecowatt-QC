# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 03:43:22 2023.

Script to get historical weather data (2019-2022) for 6 cities in the province
of Québec in Canada: Montreal, Quebec, Gatineau, Sherbrooke, Saguenay and
Trois-Rivieres. 

Instructions from Weather Canada:
Hourly data interval:
for year in `seq 1998 2008`;
    do for month in `seq 1 12`;
        do wget --content-disposition 
        "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&
        stationID=1706&Year=${year}&Month=${month}&Day=14&timeframe=1&submit= Download+Data"
        ;done;done

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
    Cities = ['Montreal', 'Quebec', 'Gatineau', 'Sherbrooke', 'Saguenay',
              'Trois-Rivieres']
    StationIDs = [51157, 51457, 53001, 48371, 5911, 51698]
    Months = list(range(1,13,1))
    Years = list(range(2019,2023,1))
    
    # Requests
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    i = 0
    for stationID in tqdm(StationIDs):
        df = pd.DataFrame()
        for year in Years:
            for month in Months:
                query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
                api_endpoint = base_url + query_url
                df_temp = pd.read_csv(api_endpoint)
                df_temp = df_temp[['Station Name','Date/Time (LST)','Temp (°C)']]
                df = pd.concat([df,df_temp],axis=0)
                pass # end of for month in Months
            pass # end of for year in Years
        df.to_csv(Cities[i]+'_2019to2022.csv')
        i+=1
        pass # end of for stationID in tqdm(StationIDs)
    
    pass # end of Main program
