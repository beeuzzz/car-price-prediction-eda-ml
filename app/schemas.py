"""Kontrakt API. Nazwy pól odpowiadają kolumnom modelu, poza dwoma wyjątkami:
- rok_produkcji (model uczył się na wieku auta),
- poziom_wyposazenia (kolumna ilosc_wyposazenia).
Wyposażenie jest przyjmowane jako bool, nie jako "Tak"/"Nie".
"""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app import model_service
from src.config import MAX_CAR_AGE

CURRENT_YEAR = date.today().year
OLDEST_YEAR = CURRENT_YEAR - MAX_CAR_AGE


class Equipment(BaseModel):
    """Elementy wyposażenia sterowane checkboxami."""

    model_config = ConfigDict(extra="forbid")

    skorzana_tapicerka: bool = False
    serwis_aso: bool = False
    dach_panoramiczny: bool = False
    swiatla_led: bool = False
    swiatla_tylne_led: bool = False
    pierwszy_wlasciciel: bool = False
    klimatyzacja_automatyczna: bool = False
    kamera_cofania: bool = False
    podgrzewane_fotele: bool = False
    tempomat: bool = False
    aktywny_tempomat: bool = False
    czytanie_znakow: bool = False
    ladowarka_indukcyjna: bool = False
    android_auto: bool = False


class CarFeaturesIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    marka: str
    rok_produkcji: int = Field(ge=OLDEST_YEAR, le=CURRENT_YEAR)
    przebieg: float = Field(ge=0, le=1_000_000)

    pojemnosc_silnika: float | None = Field(default=None, ge=400, le=8000)
    moc_silnika: float | None = Field(default=None, ge=30, le=1000)
    skrzynia_biegow: str | None = None
    paliwo: str | None = None
    naped: str | None = None
    wojewodztwo: str | None = None
    nadwozie: str | None = None
    kolor: str | None = None
    typ_sprzedawcy: str | None = None

    poziom_wyposazenia: int | None = Field(default=None, ge=0, le=150)
    importowany: bool = False
    wyposazenie: Equipment = Field(default_factory=Equipment)

    @model_validator(mode="after")
    def validate_against_model_categories(self):
        """Sprawdza wartości kategoryczne względem kategorii znanych modelowi.

        Bez tego nieznana wartość przechodzi przez OneHotEncoder z handle_unknown='ignore'
        jako wektor zer - żądanie kończy się sukcesem, a wycena jest po cichu zaniżona.
        """
        if not model_service.is_ready():
            return self

        problems = []
        for column, allowed in model_service.category_options().items():
            value = getattr(self, column, None)
            if value is not None and value not in allowed:
                problems.append(
                    f"{column}: '{value}' nie jest wartością znaną modelowi "
                    f"(dozwolone: {', '.join(allowed)})"
                )

        if problems:
            raise ValueError("; ".join(problems))

        return self


class PriceRange(BaseModel):
    od: int
    do: int


class PredictionOut(BaseModel):
    przewidywana_cena: int
    waluta: str
    przedzial: PriceRange
    model_version: str
    ostrzezenia: list[str]


class FormOptionsOut(BaseModel):
    kategorie: dict[str, list[str]]
    etykiety_kategorii: dict[str, str]
    etykiety_wartosci: dict[str, dict[str, str]]
    zakresy: dict[str, dict[str, float]]
    ograniczenia: dict[str, object]
    wyposazenie: list[dict[str, str]]
    presety_wyposazenia: list[dict[str, object]]


class ModelInfoOut(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_name: str
    train_timestamp: str
    train_shape: list[int]
    liczba_cech_wejsciowych: int
    metryki_testowe: dict[str, float]
    wersje_bibliotek: dict[str, str]
