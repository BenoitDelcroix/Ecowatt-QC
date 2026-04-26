# Ecowatt-QC

Ecowatt-QC is a Streamlit web application inspired by the French Écowatt project (https://www.monecowatt.fr/), adapted for the province of Quebec. It provides real-time visualization and 24-hour forecasts of electricity demand using open data from Hydro-Québec and Weather Canada.

## Features

- **Real-time visualization** of Quebec's electricity demand
- **24-hour demand forecasts** with grid stress indicators
- **Interactive graphs** (Plotly) and data tables
- **Custom scenarios**: adjust production capacity to test different cases

## Project Structure

```
.
├── Data/
│   ├── ElectricityDemand/         # Historical demand data and scripts
│   ├── ElectricityProduction/     # Historical production data and scripts
│   ├── HQ_ProductionCapacity/     # Hydro-Québec production capacity
│   ├── Population/                # Demographic data
│   └── Weather/                   # Weather data and scripts
├── Images/                        # UI images (traffic lights, etc.)
├── Models/                        # Saved ML models (joblib)
├── StreamlitApp-Ecowatt-QC.py     # Main Streamlit app
├── ModelTraining.py               # Model training script
├── PrepareDatasetForTraining.py   # Dataset preparation script
├── pyproject.toml                 # Python dependencies and config
└── requirements.txt               # (optional) Alternative dependencies
```

## Installation

1. **Clone the repository**
   ```
   git clone https://github.com/BenoitDelcroix/Ecowatt-QC.git
   cd Ecowatt-QC
   ```

2. **Create and sync the Python environment with uv**
   ```
   uv venv
   uv pip install -r pyproject.toml
   ```

3. **Run the Streamlit app**
   ```
   uv run streamlit run StreamlitApp-Ecowatt-QC.py
   ```

## Data Sources

- **Weather**: Historical and forecast data for 6 major Quebec cities (see Data/Weather)
- **Electricity demand and production**: Hydro-Québec open data (Data/ElectricityDemand, Data/ElectricityProduction)
- **Population**: Statistique Québec (Data/Population)
- **Production capacity**: Hydro-Québec (Data/HQ_ProductionCapacity)

## Models

The models are gradient-boosted decision trees (scikit-learn, joblib):
- `Models/MeanModel.joblib`
- `Models/Model_q95.joblib`
- `Models/Model_q99.joblib`

## Main dependencies

- streamlit
- pandas
- numpy
- scikit-learn
- plotly
- workalendar
- lxml

All dependencies are listed in `pyproject.toml`.

## How it works

- The app loads the latest data and models at startup.
- The user can visualize the current grid status and 24-hour forecasts.
- Grid stress is indicated by color (green, orange, red) based on demand vs. capacity.
- Forecasts use weather, calendar, and historical demand features.

## Contributing

Contributions are welcome! Please open an issue or pull request.