# Ecowatt-QC
Ecowatt made in QC  

## Data    
- Weather data (source: Meteo Canada)  
    - Montréal:  
        - Past: see folder Data  
        - Last 24 hours: https://weather.gc.ca/past_conditions/index_e.html?station=yul  
        - Current: https://weather.gc.ca/city/pages/qc-147_metric_e.html  
        - Forecast: https://weather.gc.ca/forecast/hourly/qc-147_metric_e.html    
    - Québec:  
        - Past: see folder Data  
        - Last 24 hours: https://weather.gc.ca/past_conditions/index_e.html?station=yqb    
        - Current: https://weather.gc.ca/city/pages/qc-133_metric_e.html  
        - Forecast: https://weather.gc.ca/forecast/hourly/qc-133_metric_e.htmlg      
    - Gatineau:  
        - Past: see folder Data  
        - Last 24 hours: https://weather.gc.ca/past_conditions/index_e.html?station=ynd    
        - Current: https://weather.gc.ca/city/pages/qc-126_metric_e.html  
        - Forecast: https://weather.gc.ca/forecast/hourly/qc-126_metric_e.html      
    - Sherbrooke:  
        - Past: see folder Data  
        - Last 24 hours: https://weather.gc.ca/past_conditions/index_e.html?station=ysc    
        - Current: https://weather.gc.ca/city/pages/qc-136_metric_e.html  
        - Forecast: https://weather.gc.ca/forecast/hourly/qc-136_metric_e.html      
    - Saguenay:  
        - Past: see folder Data  
        - Last 24 hours: https://weather.gc.ca/past_conditions/index_e.html?station=wjo    
        - Current: https://weather.gc.ca/city/pages/qc-166_metric_e.html  
        - Forecast: https://weather.gc.ca/forecast/hourly/qc-166_metric_e.html      
    - Trois-Rivières:  
        - Past: see folder Data  
        - Last 24 hours: https://weather.gc.ca/past_conditions/index_e.html?station=yrq    
        - Current: https://weather.gc.ca/city/pages/qc-130_metric_e.html  
        - Forecast: https://weather.gc.ca/forecast/hourly/qc-130_metric_e.html      
- Population data (source: https://statistique.quebec.ca/fr/produit/tableau/estimation-de-la-population-du-quebec)  
- Electricity use data (source: Hydro-Québec Open Data):  
    - Past: see folder Data    
    - Current: https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/demande.json    
- Electricity production data (source: Hydro-Québec Open Data):  
    - Past: see folder Data  
    - Current: https://www.hydroquebec.com/data/documents-donnees/donnees-ouvertes/json/production.json  
- Hydro-Québec production capacity (source: https://www.hydroquebec.com/production/centrales.html)  

## Methods  
### Basic method to assess grid stress  

### Method to forecast next 24-hour electricity demand  
- ML model: gradient-boosted decision trees  
- X data:  
    - Weather: for each of the 6 cities (Montréal, Québec, Gatineau, Sherbrooke, 
    Saguenay and Trois-rivières), 6 inputs: min, mean and max of the last and 
    next 24 hours (36 inputs)   
    - Population (1 input)  
    - Past 24-hour electricity demand (24 * 4 = 96 inputs)  
    - Total number of inputs: 36 + 1 + 96 = 133  
- Y data:  
    - Future 24-hour electricity demand (24 * 4 = 96 outputs)  
    - Total number of outputs: 96
### Method for deployment  
- User interface through a streamlit app  
- API through FastAPI and Deta  