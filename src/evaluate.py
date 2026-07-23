import pandas as pd
import numpy as np
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, 
    r2_score, root_mean_squared_error, mean_absolute_percentage_error
)

def calculate_metrics(y_true, y_pred, model_name):
    return {
        'Model': model_name,
        'MSE': mean_squared_error(y_true, y_pred),
        'RMSE': root_mean_squared_error(y_true, y_pred),
        'MAE': mean_absolute_error(y_true, y_pred),
        'MAPE': mean_absolute_percentage_error(y_true, y_pred) * 100,
        'R2': r2_score(y_true, y_pred)
    }

def error_analysis(X_test, y_test, y_pred):
    X_test_copy = X_test.copy()

    diff = abs(y_test - y_pred)

    X_test_copy['Cena'] = y_test
    X_test_copy['Cena przewidywana'] = y_pred
    X_test_copy['Różnica rzeczywista - przewidywana'] = diff
    X_test_copy['Różnica procentowa'] = (diff / y_test) * 100

    return X_test_copy.sort_values(by='Różnica procentowa', ascending=False)

def ocena_na_zbiorze_testowym(cale_modele, X_test, y_test):
    metryki_testowe = {}
    
    for nazwa_modelu, model in cale_modele.items():
        y_pred = model.predict(X_test)
        
        metryki_testowe[nazwa_modelu] = {
            'MAPE': mean_absolute_percentage_error(y_test, y_pred) * 100,
            'MAE': mean_absolute_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred))
        }
        
    return metryki_testowe