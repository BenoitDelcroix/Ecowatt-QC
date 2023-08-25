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
import workalendar
from datetime import datetime as dt
import plotly.graph_objects as go
import ssl
from urllib import request
import json

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
def LoadPrevWeather(year,month,day,hour):
    """
    

    Returns
    -------
    dfPrevWeather : TYPE
        DESCRIPTION.

    """
    # Definitions
    Cities = ['Montreal','Quebec','Gatineau','Sherbrooke','Saguenay',
              'Trois-Rivieres']
    Past24h = ['https://weather.gc.ca/past_conditions/index_e.html?station=yul',
               'https://weather.gc.ca/past_conditions/index_e.html?station=yqb',
               'https://weather.gc.ca/past_conditions/index_e.html?station=ynd',
               'https://weather.gc.ca/past_conditions/index_e.html?station=ysc',
               'https://weather.gc.ca/past_conditions/index_e.html?station=wjo',
               'https://weather.gc.ca/past_conditions/index_e.html?station=yrq']
    Past24h_min = []
    Past24h_mean = []
    Past24h_max = []
    
    # Get data
    for i in range(len(Past24h)):
        df_past = pd.read_html(Past24h[i])[0][['Date / Time (EDT)',
                                               'Temperature  (°C)']]
        df_past = df_past[df_past['Date / Time (EDT)'] != 
                          df_past['Temperature  (°C)']]
        df_past[['Temperature  (°C)','other']] = df_past['Temperature  (°C)'].\
        str.split('  ',expand=True)
        df_past['Temperature  (°C)'] = pd.to_numeric(df_past['Temperature  (°C)'],
                                                     errors='coerce') 
        df_past.dropna(inplace=True)
        
        Past24h_min.append(df_past['Temperature  (°C)'].min())
        Past24h_mean.append(df_past['Temperature  (°C)'].mean())
        Past24h_max.append(df_past['Temperature  (°C)'].max())
        
        pass # end of loop for i in tqdm(range(len(Past24h)))
    
    df = pd.DataFrame(data=Past24h_min,columns=['Past24h_min'],index=Cities)
    df['Past24h_mean'] = Past24h_mean
    df['Past24h_max'] = Past24h_max
    
    return df

@st.cache_data
def LoadWeatherForecast(year,month,day,hour):
    """
    

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    # Definitions
    Cities = ['Montreal','Quebec','Gatineau','Sherbrooke','Saguenay',
              'Trois-Rivieres']
    Next24h = ['https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-133_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-126_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-136_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-166_metric_e.html',
               'https://weather.gc.ca/forecast/hourly/qc-130_metric_e.html']
    Next24h_min = []
    Next24h_mean = []
    Next24h_max = []
    
    # Get data
    for i in range(len(Next24h)):
        df_future = pd.read_html(Next24h[i])[0][['Date/Time  (EDT)', 
                                                 'Temp.  (°C)']]
        df_future = df_future[df_future['Date/Time  (EDT)'] != 
                              df_future['Temp.  (°C)']]
        df_future['Temp.  (°C)'] = pd.to_numeric(df_future['Temp.  (°C)'],
                                                 errors='coerce') 
        df_future.dropna(inplace=True)
        
        Next24h_min.append(df_future['Temp.  (°C)'].min())
        Next24h_mean.append(df_future['Temp.  (°C)'].mean())
        Next24h_max.append(df_future['Temp.  (°C)'].max())
        
        pass # end of loop for i in tqdm(range(len(Past24h)))
    
    df = pd.DataFrame(data=Next24h_min,columns=['Next24h_min'],index=Cities)
    df['Next24h_mean'] = Next24h_mean
    df['Next24h_max'] = Next24h_max
    
    return df

@st.cache_data
def GetCurrentElectricityDemand(year,month,day,hour):
    """
    

    Parameters
    ----------
    year : TYPE
        DESCRIPTION.
    month : TYPE
        DESCRIPTION.
    day : TYPE
        DESCRIPTION.
    hour : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
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
    for i in raw['details']:
        try:
            listValue.append(i['valeurs']['demandeTotal'])
            listDate.append(i['date'])
        except:
            break        
        pass
    df = pd.DataFrame(data=listDate,columns=['Date'])
    df['Demand_MW'] = listValue

    return df

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
                same goal for the province of Quebec (as a preliminary 
                prototype). Using open data from Hydro-Québec and Weather 
                Canada, the app presents the current situation on the Quebec 
                power grid, as well as a forecast for the next 24 hours.  
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
    
    # Define the HQ production capacity to consider
    st.markdown("""
                ## 3. What is the HQ production capacity to consider?  
                In 2023, the total hydroelectric capacity in Quebec is 36877 
                MW (36.9 GW), excluding capacities from thermal plants, remote 
                networks and other supply. By default, this value is given in 
                the slider below. If you want to test scenarios where the 
                capacity has a different value, do not hesitate to change that 
                with the slider.  
                """)
    capacity = st.slider('What is the production capacity to consider (in GW)?', 
                         30.0, 60.0, 36.9, 0.1)
    
    # Introduce the features
    st.markdown("""
                ## 4. Features  
                ### 4.1. Feature 1 - Current situation on the grid  
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
        with st.spinner('Getting current electricity demand data...'):
            dfCurDemand = GetCurrentElectricityDemand(dt.utcnow().year,
                                                      dt.utcnow().month,
                                                      dt.utcnow().day,
                                                      dt.utcnow().hour)    
        st.success('Current electricity demand data obtained')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Time series  ')
            st.dataframe(dfCurDemand)
            pass
        with col2:
            st.markdown("""
                        ### Visual indicator  
                        Gauge presenting the current situation on the grid. To 
                        be noted: the thin black line presents the production 
                        capacity defined by the slider above.  
                        """)
            fig = go.Figure(go.Indicator(domain = {'x': [0, 1], 'y': [0, 1]},
                                         value = dfCurDemand['Demand_MW'].\
                                             values[-1]/1000,
                                         mode = "gauge+number",
                                         title = {'text': 'Current situation on'+\
                                                  ' the network [GW]'},
                                         gauge = {'axis': {'range': [None, 60]},
                                                  'bar': {'color': "black"},
                                                  'steps' : [{'range': [0, 0.8*capacity],
                                                              'color': "green"},
                                                             {'range': [0.8*capacity, 0.95*capacity],
                                                              'color': "orange"},
                                                             {'range': [0.95*capacity, 60],
                                                              'color': "red"}],
                                                  'threshold': {'line': {'color': "black", 
                                                                         'width': 4},
                                                                'thickness': 0.75,
                                                                'value': capacity}}))
            st.plotly_chart(fig)
            pass
    
        pass # end of currentSituation
    
    # Second section - Forecast for the next 24 hours
    st.markdown("""
                ### 4.2. Feature 2 - Forecast for the next 24 hours  
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
        with st.spinner('Getting weather data from the last 24 hours...'):
            dfPrevWeather = LoadPrevWeather(dt.utcnow().year,dt.utcnow().month,
                                            dt.utcnow().day,dt.utcnow().hour)    
        st.success('Previous weather data obtained')
                
        with st.spinner('Getting weather data for the next 24 hours...'):
            dfWeatherForecast = LoadWeatherForecast(dt.utcnow().year,
                                                    dt.utcnow().month,
                                                    dt.utcnow().day,
                                                    dt.utcnow().hour)
        st.success('Weather forecast data obtained')
        
        with st.spinner('Getting current electricity demand data...'):
            dfCurDemand = GetCurrentElectricityDemand(dt.utcnow().year,
                                                      dt.utcnow().month,
                                                      dt.utcnow().day,
                                                      dt.utcnow().hour)    
        st.success('Current electricity demand data obtained')
        dfCurDemand['Date'] = pd.to_datetime(dfCurDemand['Date'])
        dfCurDemand.set_index('Date',inplace=True)
        dfCurDemand = dfCurDemand.resample('H').mean()
        
        st.markdown("""
                    #### Data used to estimate the future situation  
                    """)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('Statistics of weather conditions from the last 24 hours  ')
            st.dataframe(dfPrevWeather)
        with col2:
            st.markdown('Statistics of weather conditions for the next 24 hours  ')
            st.dataframe(dfWeatherForecast)
        with col3:
            st.markdown('Average hourly electricity demand for the last hours  ')
            st.dataframe(dfCurDemand)
            
        st.markdown("""
                    #### Estimations for the next 24 hours    
                    """)
        
        pass # end of currentSituation
    
    
    pass # end of main program
