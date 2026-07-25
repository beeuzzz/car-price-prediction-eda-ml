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
from src.evaluate import calculate_metrics


def train_and_save_model(X_train, y_train, X_test, y_test, preprocessor, target_model, numeric_columns, basic_categorical_columns, equipment_categorical_columns):
    print("Starting to build and train the final pipeline...")

    pipeline_steps = list(preprocessor.steps) + [("Model", target_model)]
    final_pipeline = ImbPipeline(steps=pipeline_steps)

    final_pipeline.fit(X_train, y_train)
    print("Training completed.")


    test_metrics = calculate_metrics(y_test, final_pipeline.predict(X_test), type(target_model.regressor).__name__)

    column_categories = {
        col: list(X_train[col].unique())
        for col in X_train.select_dtypes(include=["object", "category", "string"])
    }

    metadata = {
        "model_name": type(target_model.regressor).__name__,
        "target_name": "cena",
        'kolumny_wejsciowe_wszystkie': list(X_train.columns),
        'kolumny_numeryczne': numeric_columns,
        'kolumny_kategoryczne_podstawowe': basic_categorical_columns,
        'kolumny_kategoryczne_wyposazenie': equipment_categorical_columns,
        "dtypes": X_train.dtypes.astype(str).to_dict(),
        "train_shape": X_train.shape,
        "test_metrics": test_metrics,
        "test_size": 0.2,
        "random_state": RANDOM_STATE,
        "kategorie_kolumn": column_categories,
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

    joblib.dump(final_pipeline, 'models/car_price_model.pkl')
    joblib.dump(metadata, 'models/model_metadata.pkl')

    print("Model and metadata saved to the 'models/' directory.")

    return final_pipeline
