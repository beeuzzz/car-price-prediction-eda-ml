from pathlib import Path
import pandas as pd
import numpy as np
from src.config import (
    MIN_CENA,
    MAX_CENA,
    MAX_WIEK_AUTA,
    MIN_PRZEBIEG,
    WYKLUCZONE_PALIWA,
    WYKLUCZONE_KRAJE_POCHODZENIA
)

# Wczytujemy dane z pliku CSV
read_path = Path("data/dane_ogloszen_po_ekstrakcji.csv")
df = pd.read_csv(read_path)


''' Czyszczenie i transformacja danych '''

# Cena jest w formacie tekstowym, usuwamy znaki niebędące cyframi i kropką, a następnie konwertujemy na typ float
df['cena'] = df['cena'].str.replace(r'[^\d.]', '', regex=True).astype(float)

# Pojemność silnika jest w formacie tekstowym, usuwamy znaki niebędące cyframi i kropką, a następnie konwertujemy na typ float
df['pojemnosc_silnika'] = df['pojemnosc_silnika'].str.replace(r'[^\d.]', '', regex=True)
df['pojemnosc_silnika'] = df['pojemnosc_silnika'].str[:-1].astype(float)

# Przebieg jest w formacie tekstowym, usuwamy znaki niebędące cyframi i kropką, a następnie konwertujemy na typ float
df['przebieg'] = df['przebieg'].str.replace(r'[^\d.]', '', regex=True).astype(float)

# Moc silnika jest w formacie tekstowym, usuwamy znaki niebędące cyframi i kropką, a następnie konwertujemy na typ float
df['moc_silnika'] = df['moc_silnika'].str.replace(r'[^\d.]', '', regex=True).astype(float)

# Zamieniamy kolumnę "RokProdukcji" na "WiekAuta"
df["rok_produkcji"] = pd.Timestamp.now().year - df["rok_produkcji"]
df.rename(columns={"rok_produkcji": "wiek_auta"}, inplace=True)

# Skracamy nazwy niektórych kategorii w kolumnie "naped" dla lepszej czytelności
df["naped"] = np.where(df["naped"] == "4x4 (dołączany automatycznie)", "4x4 (automatyczny)", df["naped"])
df["naped"] = np.where(df["naped"] == "4x4 (dołączany ręcznie)", "4x4 (ręczny)", df["naped"])

### Zmieniamy kolumnę "importowany" na zmienną binarną.
df['importowany'] = np.where(df['importowany'] == 'Importowany', "Tak", "Nie")


'''Wprowadzamy ograniczenia, w celu optymalizacji wyników potencjalnego modelu.'''

### Rezygnujemy z predykcji aut elektrycznych, ponieważ ich liczba w zbiorze danych jest zbyt mała.
maska = ~df['paliwo'].isin(WYKLUCZONE_PALIWA)
df = df[maska]

### Predykcja cen aut uszkodzonych wymaga dodatkowych danych obrazujących stopień uszkodzeń, niestety zbiór danych tego nie uwzględnia 
maska = ~df['uszkodzony'].isin(['Tak'])
df = df[maska]
df = df.drop(columns='uszkodzony')

### Ograniczamy zmienną celu Cena do przedziału 15 000 - 400 000, ponieważ w tym zakresie znajduje się większość danych, a wartości odstające mogą zaburzać wyniki modelu.
maska = (df["cena"] >= MIN_CENA) & (df["cena"] <= MAX_CENA)
df = df[maska]

### Wprowadzamy ograniczenie wieku pojazdu, ponieważ ich uwzględnienie zaburzało znacząco wyniki modelu. Wiek auta ograniczamy do 25 lat.
maska = df["wiek_auta"] <= MAX_WIEK_AUTA
df = df[maska]

### Model ma uwzględniać predykcję pojazdów używanych, pojazdy poniżej 5000 km są praktycznie nowe.
maska = df["przebieg"] >= MIN_PRZEBIEG
df = df[maska]

### Ogłoszenia pojazdów z USA to w masowej skali propozycje sprowadzenia, gdzie cena nie uwzględnia potrzebnych opłat np. celnych, pozostawienie ich w modelu obniża skutczność.
maska = ~df['importowany'].isin(WYKLUCZONE_KRAJE_POCHODZENIA)
df = df[maska]

### Pozbywamy się duplikatów
df = df.drop_duplicates()

### Zapisujemy przetworzone dane do nowego pliku CSV
save_path = Path("data/dane_ogloszen_po_transformacji.csv")
df.to_csv(save_path, index=False)

