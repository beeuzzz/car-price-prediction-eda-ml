"""Etykiety prezentacyjne dla formularza - warstwa czysto widokowa."""

CATEGORY_LABELS = {
    "marka": "Marka",
    "skrzynia_biegow": "Skrzynia biegów",
    "paliwo": "Rodzaj paliwa",
    "naped": "Napęd",
    "wojewodztwo": "Województwo",
    "nadwozie": "Typ nadwozia",
    "kolor": "Kolor",
    "typ_sprzedawcy": "Typ sprzedawcy",
}

VALUE_LABELS = {
    "typ_sprzedawcy": {
        "PRIVATE": "Osoba prywatna",
        "PROFESSIONAL": "Dealer / firma",
    },
}

EQUIPMENT_LABELS = {
    "skorzana_tapicerka": "Tapicerka skórzana",
    "serwis_aso": "Serwisowany w ASO",
    "dach_panoramiczny": "Dach panoramiczny",
    "swiatla_led": "Światła LED (przednie)",
    "swiatla_tylne_led": "Światła LED (tylne)",
    "pierwszy_wlasciciel": "Pierwszy właściciel",
    "klimatyzacja_automatyczna": "Klimatyzacja automatyczna",
    "kamera_cofania": "Kamera cofania",
    "podgrzewane_fotele": "Podgrzewane fotele",
    "tempomat": "Tempomat",
    "aktywny_tempomat": "Tempomat adaptacyjny",
    "czytanie_znakow": "Rozpoznawanie znaków",
    "ladowarka_indukcyjna": "Ładowarka indukcyjna",
    "android_auto": "Android Auto / CarPlay",
}

EQUIPMENT_PRESETS = [
    {"wartosc": 15, "etykieta": "Bazowe"},
    {"wartosc": 38, "etykieta": "Średnie"},
    {"wartosc": 60, "etykieta": "Bogate"},
    {"wartosc": 90, "etykieta": "Topowe"},
]
