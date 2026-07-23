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

# Wczytujemy dane z pliku CSV
read_path = Path("data/extracted_listings.csv")
car_price_dataframe = pd.read_csv(read_path)


''' Czyszczenie i transformacja danych '''

# Cena jest w formacie tekstowym, usuwamy znaki niebędące cyframi i kropką, a następnie konwertujemy na typ float
car_price_dataframe['cena'] = car_price_dataframe['cena'].str.replace(r'[^\d.]', '', regex=True).astype(float)

# Pojemność silnika jest w formacie tekstowym, usuwamy znaki niebędące cyframi i kropką, a następnie konwertujemy na typ float
car_price_dataframe['pojemnosc_silnika'] = car_price_dataframe['pojemnosc_silnika'].str.replace(r'[^\d.]', '', regex=True)
car_price_dataframe['pojemnosc_silnika'] = car_price_dataframe['pojemnosc_silnika'].str[:-1].astype(float)

# Przebieg jest w formacie tekstowym, usuwamy znaki niebędące cyframi i kropką, a następnie konwertujemy na typ float
car_price_dataframe['przebieg'] = car_price_dataframe['przebieg'].str.replace(r'[^\d.]', '', regex=True).astype(float)

# Moc silnika jest w formacie tekstowym, usuwamy znaki niebędące cyframi i kropką, a następnie konwertujemy na typ float
car_price_dataframe['moc_silnika'] = car_price_dataframe['moc_silnika'].str.replace(r'[^\d.]', '', regex=True).astype(float)

# Zamieniamy kolumnę "RokProdukcji" na "WiekAuta"
car_price_dataframe["rok_produkcji"] = pd.Timestamp.now().year - car_price_dataframe["rok_produkcji"]
car_price_dataframe.rename(columns={"rok_produkcji": "wiek_auta"}, inplace=True)

# Skracamy nazwy niektórych kategorii w kolumnie "naped" dla lepszej czytelności
car_price_dataframe["naped"] = np.where(car_price_dataframe["naped"] == "4x4 (dołączany automatycznie)", "4x4 (automatyczny)", car_price_dataframe["naped"])
car_price_dataframe["naped"] = np.where(car_price_dataframe["naped"] == "4x4 (dołączany ręcznie)", "4x4 (ręczny)", car_price_dataframe["naped"])

### Zmieniamy kolumnę "importowany" na zmienną binarną.
car_price_dataframe['importowany'] = np.where(car_price_dataframe['importowany'] == 'Importowany', "Tak", "Nie")


'''Wprowadzamy ograniczenia, w celu optymalizacji wyników potencjalnego modelu.'''

### Rezygnujemy z predykcji aut elektrycznych, ponieważ ich liczba w zbiorze danych jest zbyt mała.
mask = ~car_price_dataframe['paliwo'].isin(EXCLUDED_FUEL_TYPES)
car_price_dataframe = car_price_dataframe[mask]

### Predykcja cen aut uszkodzonych wymaga dodatkowych danych obrazujących stopień uszkodzeń, niestety zbiór danych tego nie uwzględnia
mask = ~car_price_dataframe['uszkodzony'].isin(['Tak'])
car_price_dataframe = car_price_dataframe[mask]
car_price_dataframe = car_price_dataframe.drop(columns='uszkodzony')

### Ograniczamy zmienną celu Cena do przedziału 15 000 - 400 000, ponieważ w tym zakresie znajduje się większość danych, a wartości odstające mogą zaburzać wyniki modelu.
mask = (car_price_dataframe["cena"] >= MIN_PRICE) & (car_price_dataframe["cena"] <= MAX_PRICE)
car_price_dataframe = car_price_dataframe[mask]

### Wprowadzamy ograniczenie wieku pojazdu, ponieważ ich uwzględnienie zaburzało znacząco wyniki modelu. Wiek auta ograniczamy do 25 lat.
mask = car_price_dataframe["wiek_auta"] <= MAX_CAR_AGE
car_price_dataframe = car_price_dataframe[mask]

### Model ma uwzględniać predykcję pojazdów używanych, pojazdy poniżej 5000 km są praktycznie nowe.
mask = car_price_dataframe["przebieg"] >= MIN_MILEAGE
car_price_dataframe = car_price_dataframe[mask]

### Ogłoszenia pojazdów z USA to w masowej skali propozycje sprowadzenia, gdzie cena nie uwzględnia potrzebnych opłat np. celnych, pozostawienie ich w modelu obniża skutczność.
mask = ~car_price_dataframe['importowany'].isin(EXCLUDED_COUNTRIES_OF_ORIGIN)
car_price_dataframe = car_price_dataframe[mask]

### Pozbywamy się duplikatów
car_price_dataframe = car_price_dataframe.drop_duplicates()

### Zapisujemy przetworzone dane do nowego pliku CSV
save_path = Path("data/cleaned_listings.csv")
car_price_dataframe.to_csv(save_path, index=False)
