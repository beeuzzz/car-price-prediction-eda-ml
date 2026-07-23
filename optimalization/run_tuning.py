from optimalization.hiperparameters import szukaj_hiperparametrow, zapisz_wyniki_do_json
from src.evaluate import ocena_na_zbiorze_testowym
from src.pipeline import build_preprocessing_pipeline
from sklearn.model_selection import train_test_split
import pandas as pd
from src.config import PARAM_GRID, RANDOM_STATE

if __name__ == "__main__":
    # Wczytanie danych
    df = pd.read_csv('data/dane_ogloszen_po_transformacji.csv')
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(columns=['cena']), df['cena'], test_size=0.2, random_state=RANDOM_STATE
    )

    # Budowa potoku przetwarzania danych
    preprocessor = build_preprocessing_pipeline()

    # Szukanie hiperparametrów dla modeli
    best_indices, best_params, best_metric_scores, all_models = szukaj_hiperparametrow(X_train, y_train, preprocessor, PARAM_GRID)

    best_test_metrics = ocena_na_zbiorze_testowym(all_models, X_test, y_test)

    # Zapis wyników do pliku JSON
    zapisz_wyniki_do_json(best_params, best_metric_scores, best_indices, best_test_metrics, 'wyniki_optymalizacji.json')