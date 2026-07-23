import pandas as pd
from sklearn.model_selection import train_test_split
from src.pipeline import build_preprocessing_pipeline
from src.train import train_and_save_model
from src.config import (
    GLOWNY_MODEL,
    KOLUMNY_NUMERYCZNE,
    KOLUMNY_KATEGORYCZNE_PODSTAWOWE,
    KOLUMNY_KATEGORYCZNE_WYPOSAZENIE,
    RANDOM_STATE
)

if __name__ == "__main__":
    print("Ładowanie danych...")
    df = pd.read_csv('data/dane_ogloszen_po_transformacji.csv')
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(columns=['cena']), df['cena'], test_size=0.2, random_state=RANDOM_STATE
    )

    print("Budowa pipeline...")
    preprocessor= build_preprocessing_pipeline()

    print("Rozpoczęcie uczenia i optymalizacji...")
    best_model = train_and_save_model(
        X_train = X_train,
        y_train = y_train,
        preprocessor = preprocessor,
        docelowy_model = GLOWNY_MODEL,
        num_cols = KOLUMNY_NUMERYCZNE,
        cat_podstawowe = KOLUMNY_KATEGORYCZNE_PODSTAWOWE,
        cat_wyposazenie = KOLUMNY_KATEGORYCZNE_WYPOSAZENIE
    )

    print("Zakończono. Modele zapisane w katalogu models/.")