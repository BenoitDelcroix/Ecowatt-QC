# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 06:29:51 2023

Script to get the last population statistics from the province of Quebec in
Canada
Source: https://statistique.quebec.ca/fr/produit/tableau/estimation-de-la-population-du-quebec

@author: delcr
"""
###############################################################################
# LIBRAIRIES
###############################################################################
import os
import pandas as pd
import sys
import numpy as np

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
    url = 'https://statistique.quebec.ca/fr/produit/tableau/'+\
        'estimation-de-la-population-du-quebec'
    
    # Get data
    raw = pd.read_html(url)
    df1_raw = raw[0]
    df1 = pd.DataFrame(data=df1_raw[df1_raw.columns[0]].values,
                       columns=['Year']) 
    df1['Population'] = df1_raw[df1_raw.columns[1]].values
    
    df2 = pd.DataFrame(data=df1_raw[df1_raw.columns[3]].values,
                       columns=['Year']) 
    df2['Population'] = df1_raw[df1_raw.columns[4]].values
    df = pd.concat([df1,df2],axis=0)
    df['Year'] = df['Year'].str.replace('r','')
    df['Year'] = df['Year'].str.replace('p','')
    df['Year'] = pd.to_numeric(df['Year'],errors='coerce')
    df.dropna(inplace=True)
    df.reset_index(inplace=True,drop=True)
    df['Population'] = df['Population'].str.replace(' ','') 
    df['Population'] = pd.to_numeric(df['Population'],errors='coerce')
    df.dropna(inplace=True)
    df.sort_values(by='Year', ascending=True)
    
    # Calculate the mean growing rate
    diffYear = np.diff(df['Year'].values)
    diffPop = np.diff(df['Population'].values)
    df_grow = pd.DataFrame(data=df['Year'].values[:-1], columns=['Year'])
    df_grow['Init_Pop'] = df['Population'].values[:-1]
    df_grow['AbsoluteDifference'] = diffPop
    df_grow['NumberYears'] = diffYear
    df_grow['MeanAnnualPerc'] = df_grow['AbsoluteDifference']/\
        df_grow['Init_Pop']*100/df_grow['NumberYears']
    MeanAnnualGrowingRate = df_grow['MeanAnnualPerc'].mean()
    
