# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 09:32:05 2023

Script to prepare a complete dataset to train a model forecasting next 24-hour
electricity demand (4*24 = 96 outputs) based on:
    - Weather (36 inputs) 
    - Population (1 input)
    - Previous electricity demand (96 inputs)
    - Beginning hour of the prediction (1 input)
    - Beginning number of day of the prediction (1 input)
    - Total number of inputs: 135

@author: delcr
"""
###############################################################################
# LIBRAIRIES
###############################################################################
import os
import pandas as pd
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
