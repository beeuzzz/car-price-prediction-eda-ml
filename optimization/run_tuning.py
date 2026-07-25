from optimization.hyperparameters import search_hyperparameters, save_results_to_json
from src.evaluate import evaluate_on_test_set
from src.pipeline import build_preprocessing_pipeline
from sklearn.model_selection import train_test_split
import pandas as pd
from src.config import PARAM_GRID, RANDOM_STATE

if __name__ == "__main__":
    car_price_dataframe = pd.read_csv('data/cleaned_listings.csv')
    X_train, X_test, y_train, y_test = train_test_split(
        car_price_dataframe.drop(columns=['cena']), car_price_dataframe['cena'], test_size=0.2, random_state=RANDOM_STATE
    )

    preprocessor = build_preprocessing_pipeline()

    best_indices, best_params, best_metric_scores, all_models = search_hyperparameters(X_train, y_train, preprocessor, PARAM_GRID)

    best_test_metrics = evaluate_on_test_set(all_models, X_test, y_test)

    save_results_to_json(best_params, best_metric_scores, best_indices, best_test_metrics, 'tuning_results.json')
