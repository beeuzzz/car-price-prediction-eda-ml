from pathlib import Path
import pandas as pd
import numpy as np
from src.config import (
    MIN_PRICE,
    MAX_PRICE,
    MAX_CAR_AGE,
    MIN_MILEAGE,
    EXCLUDED_FUEL_TYPES,
    EXCLUDED_COUNTRIES_OF_ORIGIN
)

read_path = Path("data/extracted_listings.csv")
car_price_dataframe = pd.read_csv(read_path)

car_price_dataframe['cena'] = car_price_dataframe['cena'].str.replace(r'[^\d.]', '', regex=True).astype(float)

car_price_dataframe['pojemnosc_silnika'] = car_price_dataframe['pojemnosc_silnika'].str.replace(r'[^\d.]', '', regex=True)
car_price_dataframe['pojemnosc_silnika'] = car_price_dataframe['pojemnosc_silnika'].str[:-1].astype(float)

car_price_dataframe['przebieg'] = car_price_dataframe['przebieg'].str.replace(r'[^\d.]', '', regex=True).astype(float)

car_price_dataframe['moc_silnika'] = car_price_dataframe['moc_silnika'].str.replace(r'[^\d.]', '', regex=True).astype(float)

car_price_dataframe["rok_produkcji"] = pd.Timestamp.now().year - car_price_dataframe["rok_produkcji"]
car_price_dataframe.rename(columns={"rok_produkcji": "wiek_auta"}, inplace=True)

car_price_dataframe["naped"] = np.where(car_price_dataframe["naped"] == "4x4 (dołączany automatycznie)", "4x4 (automatyczny)", car_price_dataframe["naped"])
car_price_dataframe["naped"] = np.where(car_price_dataframe["naped"] == "4x4 (dołączany ręcznie)", "4x4 (ręczny)", car_price_dataframe["naped"])

car_price_dataframe['importowany'] = np.where(car_price_dataframe['importowany'] == 'Importowany', "Tak", "Nie")

mask = ~car_price_dataframe['paliwo'].isin(EXCLUDED_FUEL_TYPES)
car_price_dataframe = car_price_dataframe[mask]

mask = ~car_price_dataframe['uszkodzony'].isin(['Tak'])
car_price_dataframe = car_price_dataframe[mask]
car_price_dataframe = car_price_dataframe.drop(columns='uszkodzony')

mask = (car_price_dataframe["cena"] >= MIN_PRICE) & (car_price_dataframe["cena"] <= MAX_PRICE)
car_price_dataframe = car_price_dataframe[mask]

mask = car_price_dataframe["wiek_auta"] <= MAX_CAR_AGE
car_price_dataframe = car_price_dataframe[mask]

mask = car_price_dataframe["przebieg"] >= MIN_MILEAGE
car_price_dataframe = car_price_dataframe[mask]

mask = ~car_price_dataframe['importowany'].isin(EXCLUDED_COUNTRIES_OF_ORIGIN)
car_price_dataframe = car_price_dataframe[mask]

car_price_dataframe = car_price_dataframe.drop_duplicates()

save_path = Path("data/cleaned_listings.csv")
car_price_dataframe.to_csv(save_path, index=False)
