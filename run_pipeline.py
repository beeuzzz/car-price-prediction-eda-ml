import pandas as pd
from sklearn.model_selection import train_test_split
from src.pipeline import build_preprocessing_pipeline
from src.train import train_and_save_model
from src.config import (
    MAIN_MODEL,
    NUMERIC_COLUMNS,
    BASIC_CATEGORICAL_COLUMNS,
    EQUIPMENT_CATEGORICAL_COLUMNS,
    RANDOM_STATE
)

if __name__ == "__main__":
    print("Loading data...")
    car_price_dataframe = pd.read_csv('data/cleaned_listings.csv')
    X_train, X_test, y_train, y_test = train_test_split(
        car_price_dataframe.drop(columns=['cena']), car_price_dataframe['cena'], test_size=0.2, random_state=RANDOM_STATE
    )

    print("Building pipeline...")
    preprocessor= build_preprocessing_pipeline()

    print("Starting training and optimization...")
    best_model = train_and_save_model(
        X_train = X_train,
        y_train = y_train,
        preprocessor = preprocessor,
        target_model = MAIN_MODEL,
        numeric_columns = NUMERIC_COLUMNS,
        basic_categorical_columns = BASIC_CATEGORICAL_COLUMNS,
        equipment_categorical_columns = EQUIPMENT_CATEGORICAL_COLUMNS
    )

    print("Done. Models saved in the models/ directory.")
