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

    absolute_difference = abs(y_test - y_pred)

    X_test_copy['Cena'] = y_test
    X_test_copy['Cena przewidywana'] = y_pred
    X_test_copy['Różnica rzeczywista - przewidywana'] = absolute_difference
    X_test_copy['Różnica procentowa'] = (absolute_difference / y_test) * 100

    return X_test_copy.sort_values(by='Różnica procentowa', ascending=False)

def evaluate_on_test_set(all_models, X_test, y_test):
    test_metrics = {}

    for model_name, model in all_models.items():
        y_pred = model.predict(X_test)

        test_metrics[model_name] = {
            'MAPE': mean_absolute_percentage_error(y_test, y_pred) * 100,
            'MAE': mean_absolute_error(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred))
        }

    return test_metrics
