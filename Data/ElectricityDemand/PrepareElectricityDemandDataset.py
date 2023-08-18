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
    Files = ['2019-demande-electricite-quebec.xlsx',
             '2020-demande-electricite-quebec.xlsx',
             '2021-demande-electricite-quebec.xlsx',
             '2022-demande-electricite-quebec.xlsx']
    
    # Process data
    df = pd.DataFrame()
    for file in tqdm(Files):
        idf = pd.read_excel(file)
        df = pd.concat([df,idf])
        pass
    df.set_index('Date',inplace=True)
    df.interpolate('linear',inplace=True)
    df.info()
    
    # Save data as csv
    today = date.today()
    df.to_csv(str(today)+'_AllElectricityDemandData_2019_2022.csv')
     
