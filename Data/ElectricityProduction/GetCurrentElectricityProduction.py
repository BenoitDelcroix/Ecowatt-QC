# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 07:22:53 2023

Script to get the current electricity production in the province of Quebec in
Canada
Source: https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/production.json
    
@author: delcr
"""
###############################################################################
# LIBRAIRIES
###############################################################################
import os
import pandas as pd
import ssl
from urllib import request
import json
from tqdm import tqdm
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
    url = 'https://www.hydroquebec.com/data/documents-donnees/'+\
        'donnees-ouvertes/json/production.json'
    
    # Get HTML data
    context = ssl.create_default_context()
    context.set_ciphers('AES128-SHA')
    response = request.urlopen(url, context=context)
    html = response.read()
    raw = json.loads(html)
    listDate = []
    listAutres = []
    listEolien = []
    listHydraulique = []
    listSolaire = []
    listThermique = []
    listTotal = []
    for i in tqdm(raw['details']):
        try:
            listAutres.append(i['valeurs']['autres'])
            listEolien.append(i['valeurs']['eolien'])
            listHydraulique.append(i['valeurs']['hydraulique'])
            listSolaire.append(i['valeurs']['solaire'])
            listThermique.append(i['valeurs']['thermique'])
            listTotal.append(i['valeurs']['total'])
            listDate.append(i['date'])
        except:
            break        
        pass
    length = min(len(listDate),len(listAutres),len(listEolien),
                 len(listHydraulique),len(listSolaire),len(listThermique),
                 len(listTotal))
    df = pd.DataFrame(data=listDate[:length],columns=['Date'])
    df['Autres_MW'] = listAutres[:length]  
    df['Eolien_MW'] = listEolien[:length]  
    df['Hydraulique_MW'] = listHydraulique[:length]  
    df['Solaire_MW'] = listSolaire[:length]  
    df['Thermique_MW'] = listThermique[:length]  
    df['Total_MW'] = listTotal[:length]  
