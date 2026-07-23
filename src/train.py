import sys
import pandas as pd
import numpy as np
import scipy as sp
import sklearn
import xgboost
import joblib
from datetime import datetime
from imblearn.pipeline import Pipeline as ImbPipeline

from src.config import RANDOM_STATE


def train_and_save_model(X_train, y_train, preprocessor, docelowy_model, num_cols, cat_podstawowe, cat_wyposazenie):
    print("Rozpoczęcie budowy i uczenia finalnego potoku...")
    
    # Budowa potoku z przekazanym, skonfigurowanym wcześniej modelem
    kroki_do_pipeline = list(preprocessor.steps) + [("Model", docelowy_model)]
    finalny_pipeline = ImbPipeline(steps=kroki_do_pipeline)
    
    # Jednorazowe trenowanie na całym zbiorze
    finalny_pipeline.fit(X_train, y_train)
    print("Uczenie zakończone.")

    # Budowa słownika ze słownikami unikalnych wartości
    kategorie_kolumn = {
        col: list(X_train[col].unique())
        for col in X_train.select_dtypes(include=["object", "category", "string"])
    }

    # Zbiór informacji o środowisku uczenia
    metadane = {
        "model_name": "XGBoost",
        "target_name": "cena",
        'kolumny_wejsciowe_wszystkie': list(X_train.columns),
        'kolumny_numeryczne': num_cols,
        'kolumny_kategoryczne_podstawowe': cat_podstawowe,
        'kolumny_kategoryczne_wyposazenie': cat_wyposazenie,
        "train_shape": X_train.shape,
        "test_size": 0.2, 
        "random_state": RANDOM_STATE,
        "kategorie_kolumn": kategorie_kolumn,
        "python_version": sys.version.split()[0],
        "library_versions": {
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "scipy": sp.__version__,
            "scikit-learn": sklearn.__version__,
            "joblib": joblib.__version__,
            "XGBoost": xgboost.__version__,
        },
        "train_timestamp": datetime.now().isoformat(timespec="seconds"),
    }

    # Zrzut obiektów do plików
    joblib.dump(finalny_pipeline, 'models/model_wyceny_pojazdow.pkl')
    joblib.dump(metadane, 'models/metadane_modelu.pkl')
    
    print("Zapisano model i metadane w katalogu 'models/'.")
    
    return finalny_pipeline