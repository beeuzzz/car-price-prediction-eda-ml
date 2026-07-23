from pathlib import Path
from sklearn.model_selection import KFold, GridSearchCV
from imblearn.pipeline import Pipeline as ImbPipeline
import json
from src.config import RANDOM_STATE

def search_hyperparameters(X_train, y_train, preprocessor, config_grid):
    optimized_model_parameters = {}
    optimized_model_metrics = {}
    all_models = {}
    best_indices = {}
    scoring_metrics = {
    'MAPE': 'neg_mean_absolute_percentage_error',
    'MAE': 'neg_mean_absolute_error',
    'RMSE': 'neg_root_mean_squared_error'
    }

    for model_name, model_config in config_grid.items():
        print(f"Starting Grid Search and Cross Validation optimization for: {model_name}")

        pipeline_steps = list(preprocessor.steps) + [("Model", model_config['model'])]
        cv_splitter = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
        current_pipeline = ImbPipeline(steps=pipeline_steps)

        grid_search = GridSearchCV(
            estimator=current_pipeline,
            param_grid=model_config['params'],
            cv=cv_splitter,
            scoring=scoring_metrics,
            refit='MAPE',
            n_jobs=-1
        )

        grid_search.fit(X_train, y_train)

        all_models[model_name] = grid_search.best_estimator_
        optimized_model_parameters[model_name] = grid_search.best_params_
        optimized_model_metrics[model_name] = grid_search.cv_results_
        best_indices[model_name] = grid_search.best_index_

        print(f"Completed for {model_name}. Optimal parameters: {grid_search.best_params_}")

    return best_indices, optimized_model_parameters, optimized_model_metrics, all_models


def save_results_to_json(best_params: dict, best_metric_scores: dict, best_indices: dict, test_metrics: dict, output_filename: str):
    # Inicjalizacja głównego słownika przechowującego dane wszystkich modeli
    final_results = {}

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
        final_results[model_name] = {
            'best_params': params,
            'train_metrics': {
                'MAPE': mape,
                'MAE': mae,
                'RMSE': rmse
            },
            'test_metrics': test_metrics[model_name]
        }

    # Zapis całego słownika do pliku JSON na samym końcu
    current_file_path = Path(__file__).resolve()
    output_filepath = current_file_path.parent / output_filename

    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=4, ensure_ascii=False)
