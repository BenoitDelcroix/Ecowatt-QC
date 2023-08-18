# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 12:38:28 2023

Script to get production capacities of Hydro-Québec from their website:
https://www.hydroquebec.com/production/centrales.html

@author: delcr
"""
###############################################################################
# LIBRAIRIES
###############################################################################
import os
import pandas as pd
from urllib import request
import ssl
from bs4 import BeautifulSoup
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
    
    # Definition
    url = 'https://www.hydroquebec.com/production/centrales.html'
    
    # Get HTML data
    context = ssl.create_default_context()
    context.set_ciphers('AES128-SHA')
    response = request.urlopen(url, context=context)
    html = response.read()
    
    # Get the first 2 tables
    tables = pd.read_html(html)
    df1 = tables[0]
    df2 = tables[1]
    df1['Puissance_MW'] = df1[df1.columns[4]].str.strip()
    df1['Puissance_MW'] = df1['Puissance_MW'].str.replace('\xa0','')
    df1['Puissance_MW'] = df1['Puissance_MW'].str.replace(' ','')
    df1['Puissance_MW'] = pd.to_numeric(df1['Puissance_MW'])
    Tot_HQ = df1['Puissance_MW'].sum()
    Tot_TGV = df2['Puissance (MW)'].values[0]
    Tot_ReseauIsole = df2['Puissance (MW)'].values[1]
    
    # Get the last table which is not a HTML table 
    soup = BeautifulSoup(html, 'html.parser')
    html_table = soup.find('ul',class_='hq-liste-donnees')
    li_elements = html_table.find_all('li')
    df3 = pd.DataFrame()
    for i in li_elements:
        # Obtenez les éléments <span> pour le titre et la valeur
        title_element = i.find('span', class_='txt')
        value_element = i.find('span', class_='nbr')
        # Ajoutez une nouvelle ligne au tableau avec le titre et la valeur
        df3 = df3.append({'Title': title_element.text, 
                          'Value': value_element.text},
                         ignore_index=True)
        pass # end of loop for i in li_elements
    df3['Value'] = df3['Value'].str.strip()
    df3['Value'] = df3['Value'].str.replace('\xa0','')
    df3['Puissance_MW'] = df3['Value'].str.extract('(\d+)')
    df3['Puissance_MW'] = pd.to_numeric(df3['Puissance_MW'])
    Tot_Autres = df3['Puissance_MW'].values[0]
    
    
    
    