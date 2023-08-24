# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 11:03:11 2023

Script defining how the Streamlit app "Ecowatt-QC" works.

@author: delcr
"""
###############################################################################
# LIBRAIRIES
###############################################################################
import os
import pandas as pd
from joblib import load
import streamlit as st
import sys
import path

###############################################################################
# FONCTIONS
###############################################################################
@st.cache_resource
def LoadModels():
    """
    

    Returns
    -------
    MeanModel : TYPE
        DESCRIPTION.
    Model_q95 : TYPE
        DESCRIPTION.
    Model_q99 : TYPE
        DESCRIPTION.

    """
    MeanModel = load(r'Models/MeanModel.joblib') 
    Model_q95 = load(r'Models/Model_q95.joblib') 
    Model_q99 = load(r'Models/Model_q99.joblib') 
    
    return MeanModel, Model_q95, Model_q99

@st.cache_data
def LoadPreviousWeather():
    """
    

    Returns
    -------
    dfPrevWeather : TYPE
        DESCRIPTION.

    """
    dfPrevWeather = pd.DataFrame()
    
    return dfPrevWeather

@st.cache_data
def LoadWeatherForecast():
    """
    

    Returns
    -------
    dfWeatherForecast : TYPE
        DESCRIPTION.

    """
    dfWeatherForecast = []
    
    return dfWeatherForecast

###############################################################################
# PROGRAMME PRINCIPAL
###############################################################################
if __name__ == "__main__":
    
    # Définir le working directory 
    cwd = os.path.abspath(os.path.dirname(__file__))
    os.chdir(cwd)
    
    # Introduction
    st.set_page_config(page_title="Ecowatt-QC", layout="wide", 
                       initial_sidebar_state="auto")
    st.markdown(""" 
                # Ecowatt-QC  
                ## 1. Introduction
                Like the Écowatt website (https://www.monecowatt.fr/) developed
                by RTE in France, this web app humbly attempts to achieve the 
                same goal for the province of Quebec. Using open data from 
                Hydro-Québec and Weather Canada, the app presents the current 
                situation on the Quebec power grid, as well as a forecast for 
                the next 24 hours.  
                ## 2. Disclaimer  
                The software is provided "as is", without warranty of any kind, 
                express or implied, including but not limited to the warranties 
                of merchantability, fitness for a particular purpose and 
                noninfringement. In no event shall the authors or copyright 
                holders be liable for any claim, damages or other liability, 
                whether in an action of contract, tort or otherwise, arising 
                from, out of or in connection with the software or the use or 
                other dealings in the software.  
                """)
    
    # Load models
    MeanModel, Model_q95, Model_q99 = LoadModels()
    
    # Introduce the features
    st.markdown("""
                ## 3. Features  
                ### 3.1. Feature 1 - Current situation on the grid  
                By checking the box herebelow, the first feature will be 
                unlocked, presenting briefly the current situation on the 
                network.   
                """)
    
    # First section - Current situation on the grid
    currentSituation = st.checkbox('Current situation on the grid')
    if currentSituation:
        st.markdown("""
                    Section to present the current situation on the network.  
                    """)
        
        pass # end of currentSituation
    
    # Second section - Forecast for the next 24 hours
    st.markdown("""
                ### 3.2. Feature 2 - Forecast for the next 24 hours  
                By checking the box herebelow, the second feature will be 
                unlocked, presenting briefly the forecasted situation on the 
                network for the next 24 hours. 
                """)
    forecastSituation = st.checkbox('Forecast for the next 24 hours')
    if forecastSituation:
        st.markdown("""
                    Section to present the forecasted situation on the network 
                    for the next 24 hours.
                    """)
        
        pass # end of currentSituation
    
    
    pass # end of main program
