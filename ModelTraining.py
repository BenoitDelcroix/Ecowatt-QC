# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 03:13:19 2023

Script to train a model forecasting the electricity demand differences between
the next and last 24 hours.

@author: delcr
"""
###############################################################################
# LIBRAIRIES
###############################################################################
import os
import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from joblib import dump

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
    
    # Load data and shuffle
    df = pd.read_csv('ProcessedTrainingDataset.csv',index_col=0)
    Inputs = list(df.columns[:41])
    Outputs = list(df.columns[41:])
    X_train, X_test, y_train, y_test = train_test_split(df[Inputs],df[Outputs], 
                                                        test_size=0.2, 
                                                        random_state=0,
                                                        shuffle=True)
    
    # Define and train models
    print('Model training - Mean model')
    model_mean = MultiOutputRegressor(
        HistGradientBoostingRegressor(loss='squared_error', quantile=None, 
                                      learning_rate=0.1, max_iter=500, 
                                      categorical_features=['BeginningHour_Forecast',
                                      'BeginningDay_Forecast','Workingday_Prev',
                                      'Workingday_Current','Workingday_Next'], 
                                      early_stopping=True, scoring='loss', 
                                      validation_fraction=0.2, n_iter_no_change=10, 
                                      tol=1e-07, verbose=0, random_state=0))
    model_mean.fit(X_train,y_train)
    print('Mean model score [R²]: '+str(model_mean.score(X_test,y_test)))
    print('Model training - Quantile model q=0.95')
    model_q95 = MultiOutputRegressor(
        HistGradientBoostingRegressor(loss='quantile', quantile=0.95, 
                                      learning_rate=0.1, max_iter=500, 
                                      categorical_features=['BeginningHour_Forecast',
                                      'BeginningDay_Forecast','Workingday_Prev',
                                      'Workingday_Current','Workingday_Next'], 
                                      early_stopping=True, scoring='loss', 
                                      validation_fraction=0.2, n_iter_no_change=10, 
                                      tol=1e-07, verbose=0, random_state=0))
    model_q95.fit(X_train,y_train)
    print('Model training - Quantile model q=0.99')
    model_q99 = MultiOutputRegressor(
        HistGradientBoostingRegressor(loss='quantile', quantile=0.99, 
                                      learning_rate=0.1, max_iter=500, 
                                      categorical_features=['BeginningHour_Forecast',
                                      'BeginningDay_Forecast','Workingday_Prev',
                                      'Workingday_Current','Workingday_Next'], 
                                      early_stopping=True, scoring='loss', 
                                      validation_fraction=0.2, n_iter_no_change=10, 
                                      tol=1e-07, verbose=0, random_state=0))
    model_q99.fit(X_train,y_train)
    print('End of training')

    # Save model
    dump(model_mean,'MeanModel.joblib')
    dump(model_q95,'Model_q95.joblib')
    dump(model_q99,'Model_q99.joblib')
    
    # Plot real data vs. simulated data - Test dataset
    plt.Figure()
    plt.scatter(y_test.values.flatten(), model_mean.predict(X_test).flatten())
    plt.title('Real data vs. Mean model')
    plt.xlabel('Real data - power difference (MW)')
    plt.ylabel('Simulated data - power difference (MW)')
    plt.show()
    
    pass # end of main program