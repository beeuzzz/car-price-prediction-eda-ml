## Model regresji wspomagający wycenę pojazdów na rynku wtórnym 

### Opis wstępny 
Celem niniejszego projektu jest opracowanie modelu estymacji wartości pojazdów w oparciu o dane pozyskane z polskiego rynku ogłoszeń motoryzacyjnych. 

Analizując kluczowe parametry techniczne i wyposażeniowe, narzędzie docelowo ma umożliwiać określenie realnej wartości rynkowej samochodu. 

Rozwiązanie to znajduje zastosowanie dla sprzedających profesjonalnych w optymalizacji oferty pod względem cenowym, oraz dla kupujących służy jako efektywne narzędzie do identyfikacji korzystynych ofert. Narzędzie te chroni ich również przed przepłaceniem za pojazd. 

### Dane
Dane wykorzystane do wytrenowania modelu pochodzą z publicznych ogłoszeń motoryzacyjnych w serwisie Otomoto i zostały pozyskane wyłącznie na niekomercyjne potrzeby realizacji tego projektu akademickiego. Zbiór danych zawiera około 3500 obserwacji oraz 30 parametrów.

### Zmienne użyte w modelu
| Zmienna objaśniające| Typ zmiennej | Opis |
| :--- | :--- | :--- |
| **Wiek auta** | Numeryczna | Liczba lat, które upłynęły od roku produkcji pojazdu. |
| **Pojemność silnika** | Numeryczna | Pojemność skokowa silnika wyrażona w centymetrach sześciennych (cm3). |
| **przebieg** | Numeryczna | Całkowity dystans w kilometrach pokonany dotychczas przez pojazd. |
| **Moc silnika** | Numeryczna | Moc jednostki napędowej wyrażona w koniach mechanicznych (KM). |
| **Ilość wyposażenia** | Numeryczna | Liczba zliczonych elementów wyposażenia dodatkowego w pojeździe. |
| **Liczba drzwi** | Numeryczna | Całkowita liczba drzwi w nadwoziu pojazdu. |
| **Marka** | Kategoryczna | Producent pojazdu określający jego prestiż i segment rynkowy. |
| **Skrzynia biegów** | Kategoryczna | Rodzaj przekładni zastosowanej w aucie (np. manualna, automatyczna). |
| **Paliwo** | Kategoryczna | Typ paliwa zasilającego silnik (np. Benzyna, Diesel, LPG, Hybryda, Elektryczny). |
| **Napęd** | Kategoryczna | Oznaczenie osi napędzanej (np. na przednie koła, na tylne koła, 4x4). |
| **Województwo** | Kategoryczna | Region rejestracji lub sprzedaży pojazdu na terenie Polski. |
| **Nadwozie** | Kategoryczna | Typ budowy pojazdu (np. Sedan, Kombi, SUV, Hatchback). |
| **Kolor** | Kategoryczna | Barwa lakieru nadwozia pojazdu. |
| **Czy uszkodzony** | Kategoryczna | Informacja, czy pojazd posiada uszkodzenia blacharskie lub mechaniczne (Tak/Nie). |
| **Typ sprzedawcy** | Kategoryczna | Profesjonalny lub prywatny sprzedawca |
| **Skórzana tapicerka** | Kategoryczna | Obecność wykończenia foteli materiałem skórzanym (Tak/Nie). |
| **Importowany** | Kategoryczna | Czy pojazd jest z polskiego salonu (Tak/Nie). |
| **Serwis ASO** | Kategoryczna | Informacja, czy auto było regularnie serwisowane w Autoryzowanej Stacji Obsługi (Tak/Nie). |
| **Dach panoramiczny** | Kategoryczna | Obecność przeszklonego dachu nad przestrzenią pasażerską (Tak/Nie). |
| **Światła LED** | Kategoryczna | Obecność przednich reflektorów wykonanych w technologii LED (Tak/Nie). |
| **Pierwszy właściciel** | Kategoryczna | Informacja, czy pojazd od nowości należał tylko do jednej osoby (Tak/Nie). |
| **Klimatyzacja automatyczna** | Kategoryczna | Obecność systemu klimatyzacji sterowanej elektronicznie (Tak/Nie). |
| **Kamera cofania** | Kategoryczna | Obecność systemu wideo wspomagającego manewr cofania (Tak/Nie). |
| **Podgrzewane fotele** | Kategoryczna | Obecność funkcji elektrycznego podgrzewania przednich lub tylnych siedzeń (Tak/Nie). |
| **Tempomat** | Kategoryczna | Obecność systemu automatycznej kontroli prędkości podróżnej (Tak/Nie). |
| **Aktywny tempomat** | Kategoryczna | Obecność zaawansowanego tempomatu utrzymującego bezpieczny dystans (Tak/Nie). |
| **Czytanie znaków** | Kategoryczna | Obecność systemu rozpoznawania znaków drogowych za pomocą kamer (Tak/Nie). |
| **Ładowarka indukcyjna** | Kategoryczna | Obecność bezprzewodowego panelu do ładowania telefonu w kabinie (Tak/Nie). |
| **Światła tylne LED** | Kategoryczna | Obecność tylnych lamp wykonanych w technologii LED (Tak/Nie). |
| **Android Auto** | Kategoryczna | Obecność systemu pozwalającego na integrację smartfona z ekranem multimedialnym (Tak/Nie). |

### Ekstrakcja i transformacja danych z formatu JSON

Proces pozyskiwania i obróbki danych został podzielony na dwa etapy, realizowane przez skrypty w katalogu `przygotowanie_danych`:

1. **Ekstrakcja danych** (`ekstrakcja_ogloszen.py`): Skrypt wczytuje surowe dane z serwisu OTOMOTO w formacie JSON. Przeszukuje on i iteruje po strukturze JSON. Na ich podstawie budowana jest tabela (DataFrame), która zostaje zapisana do pliku `dane_ogloszen_po_ekstrakcji.csv`.

2. **Transformacja danych** (`transformacja_danych.py`): Po ekstrakcji, istotna część danych jest w niepożądanym formacie (np. z walutami czy jednostkami takimi jak "km" i "cm3"). Skrypt wczytuje wstępny plik `dane_ogloszen_po_ekstrakcji.csv`. Wynik transformacji eksportowany jest do pliku `dane_ogloszen_po_transformacji.csv`, który stanowi gotowy i przygotowany zbiór pod dalszą analizę.