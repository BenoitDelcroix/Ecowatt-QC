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
    
    # Get data
    #context = ssl._create_unverified_context()
    context = ssl.create_default_context()
    context.set_ciphers('AES128-SHA')
    response = request.urlopen(url, context=context)
    html = response.read()
    tables = pd.read_html(html)
    