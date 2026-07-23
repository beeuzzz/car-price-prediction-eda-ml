from pathlib import Path
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error, mean_squared_error
import numpy as np
from sklearn.model_selection import KFold, GridSearchCV
from imblearn.pipeline import Pipeline as ImbPipeline
import json
from src.config import RANDOM_STATE

def szukaj_hiperparametrow(X_train, y_train, preprocessor, config_grid):
    parametry_modeli_po_optymalizacji = {}
    metryki_modeli_po_optymalizacji = {}
    cale_modele = {}
    best_indices = {}
    scoring_metrics = {
    'MAPE': 'neg_mean_absolute_percentage_error',
    'MAE': 'neg_mean_absolute_error',
    'RMSE': 'neg_root_mean_squared_error'
    }
    
    for nazwa_modelu, konfiguracja in config_grid.items():
        print(f"Rozpoczęcie optymalizacji Grid Search i Cross Validation dla: {nazwa_modelu}")
        
        kroki_do_pipeline = list(preprocessor.steps) + [("Model", konfiguracja['model'])]
        ramka_cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
        aktualny_pipeline = ImbPipeline(steps=kroki_do_pipeline)
        
        grid_search = GridSearchCV(
            estimator=aktualny_pipeline,
            param_grid=konfiguracja['parametry'],
            cv=ramka_cv,
            scoring=scoring_metrics,
            refit='MAPE',
            n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        
        cale_modele[nazwa_modelu] = grid_search.best_estimator_
        parametry_modeli_po_optymalizacji[nazwa_modelu] = grid_search.best_params_
        metryki_modeli_po_optymalizacji[nazwa_modelu] = grid_search.cv_results_
        best_indices[nazwa_modelu] = grid_search.best_index_
        
        print(f"Zakończono dla {nazwa_modelu}. Optymalne parametry: {grid_search.best_params_}")

    return best_indices, parametry_modeli_po_optymalizacji, metryki_modeli_po_optymalizacji, cale_modele


def zapisz_wyniki_do_json(best_params: dict, best_metric_scores: dict, best_indices: dict, test_metrics: dict, output_filename: str):
    # Inicjalizacja głównego słownika przechowującego dane wszystkich modeli
    wyniki_koncowe = {}
    
    # Dodanie .items(), aby poprawnie iterować po słowniku
    for model_name, params in best_params.items():
        
        # Pobranie indexu i wyników CV dla konkretnego modelu
        index = best_indices[model_name]
        cv_results = best_metric_scores[model_name]
        
        # Wyciągnięcie metryk. Funkcja abs() zamienia wartości negatywne na pozytywne
        mape = abs(cv_results['mean_test_MAPE'][index]) * 100
        mae = abs(cv_results['mean_test_MAE'][index])
        rmse = abs(cv_results['mean_test_RMSE'][index])
        
        # Zapisanie danych modelu do głównego słownika
        wyniki_koncowe[model_name] = {
            'best_params': params,
            'train_metrics': {
                'MAPE': mape,
                'MAE': mae,
                'RMSE': rmse
            },
            'test_metrics': test_metrics[model_name]
        }
    
    # Zapis całego słownika do pliku JSON na samym końcu
    sciezka_aktualnego_pliku = Path(__file__).resolve()
    output_filepath = sciezka_aktualnego_pliku.parent / output_filename
    
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(wyniki_koncowe, f, indent=4, ensure_ascii=False)

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