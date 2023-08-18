# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 07:22:53 2023

Script to get the current electricity demand in the province of Quebec in
Canada
Source: https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/demande.json
    
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
        'donnees-ouvertes/json/demande.json'
    
    # Get HTML data
    context = ssl.create_default_context()
    context.set_ciphers('AES128-SHA')
    response = request.urlopen(url, context=context)
    html = response.read()
    raw = json.loads(html)
    listDate = []
    listValue = []
    for i in tqdm(raw['details']):
        try:
            listValue.append(i['valeurs']['demandeTotal'])
            listDate.append(i['date'])
        except:
            break        
        pass
    df = pd.DataFrame(data=listDate,columns=['Date'])
    df['Demand_MW'] = listValue    
