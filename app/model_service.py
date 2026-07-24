"""Warstwa dostępu do wytrenowanego pipeline'u.

Jedyne miejsce w aplikacji, które dotyka pandas i artefaktów joblib. Reszta kodu
operuje na obiektach Pydantic i słownikach.
"""

import logging
from datetime import date
from typing import Any

import joblib
import pandas as pd

from app.settings import settings
from src.config import (
    BASIC_CATEGORICAL_COLUMNS,
    EQUIPMENT_CATEGORICAL_COLUMNS,
    EXCLUDED_FUEL_TYPES,
    MAX_CAR_AGE,
    MAX_PRICE,
    MIN_MILEAGE,
    MIN_PRICE,
)

logger = logging.getLogger(__name__)

EQUIPMENT_FLAGS = [column for column in EQUIPMENT_CATEGORICAL_COLUMNS if column != "importowany"]

PASSTHROUGH_CATEGORICAL = [
    "marka",
    "skrzynia_biegow",
    "paliwo",
    "naped",
    "wojewodztwo",
    "nadwozie",
    "kolor",
    "typ_sprzedawcy",
]

REQUIRED_METADATA_KEYS = (
    "kolumny_wejsciowe_wszystkie",
    "dtypes",
    "kategorie_kolumn",
    "test_metrics",
    "train_timestamp",
)

_state: dict[str, Any] = {}


def load() -> None:
    """Wczytuje model i metadane. Wywoływane raz, przy starcie aplikacji."""
    logger.info("Ładowanie artefaktów z %s", settings.model_path.parent)

    for path in (settings.model_path, settings.metadata_path):
        if not path.exists():
            raise RuntimeError(
                f"Brak artefaktu {path}. Wytrenuj model komendą: python run_pipeline.py"
            )

    _state["model"] = joblib.load(settings.model_path)
    _state["metadata"] = joblib.load(settings.metadata_path)

    missing = [key for key in REQUIRED_METADATA_KEYS if key not in _state["metadata"]]
    if missing:
        _state.clear()
        raise RuntimeError(
            f"Metadane modelu nie zawierają kluczy {missing}. "
            "Artefakt pochodzi ze starszej wersji kodu - przetrenuj: python run_pipeline.py"
        )

    logger.info(
        "Model gotowy: %s, %d cech wejściowych, trening %s",
        _state["metadata"]["model_name"],
        len(_state["metadata"]["kolumny_wejsciowe_wszystkie"]),
        _state["metadata"]["train_timestamp"],
    )


def unload() -> None:
    _state.clear()


def is_ready() -> bool:
    return "model" in _state and "metadata" in _state


def metadata() -> dict[str, Any]:
    if not is_ready():
        raise RuntimeError("Model nie jest załadowany")
    return _state["metadata"]


def warmup() -> None:
    """Pierwsza predykcja po wczytaniu jest wyraźnie wolniejsza - wykonujemy ją
    przy starcie, żeby nie trafiła w pierwszego użytkownika."""
    row = _empty_row()
    row.update({"marka": "Audi", "wiek_auta": 7, "przebieg": 120000.0})
    price = float(_state["model"].predict(_to_frame(row))[0])
    logger.info("Rozgrzewka zakończona (predykcja kontrolna: %.0f PLN)", price)


def category_options() -> dict[str, list[str]]:
    """Dozwolone wartości pól kategorycznych, odczytane z artefaktu.

    To samo źródło zasila listy rozwijane w formularzu i walidację wejścia, więc
    wartość widoczna w UI jest z definicji kategorią znaną modelowi.
    """
    categories = metadata()["kategorie_kolumn"]
    options: dict[str, list[str]] = {}

    for column in BASIC_CATEGORICAL_COLUMNS:
        values = [value for value in categories.get(column, []) if isinstance(value, str)]

        if column == "paliwo":
            values = [value for value in values if value not in EXCLUDED_FUEL_TYPES]

        options[column] = sorted(values)

    return options


def numeric_ranges() -> dict[str, dict[str, float]]:
    """Zakresy pól liczbowych - spójne z walidacją w schemas.py."""
    from app.schemas import CURRENT_YEAR, OLDEST_YEAR

    return {
        "rok_produkcji": {"min": OLDEST_YEAR, "max": CURRENT_YEAR},
        "przebieg": {"min": 0, "max": 1_000_000},
        "pojemnosc_silnika": {"min": 400, "max": 8000},
        "moc_silnika": {"min": 30, "max": 1000},
        "poziom_wyposazenia": {"min": 0, "max": 150},
    }


def constraints() -> dict[str, Any]:
    """Dziedzina, na której model był trenowany.

    Frontend pokazuje to użytkownikowi zanim zacznie wypełniać formularz - inaczej
    ograniczenia ujawniają się dopiero jako błąd walidacji po wysłaniu.
    """
    from app.schemas import CURRENT_YEAR, OLDEST_YEAR

    return {
        "min_rok": OLDEST_YEAR,
        "max_rok": CURRENT_YEAR,
        "max_wiek_auta": MAX_CAR_AGE,
        "min_przebieg": MIN_MILEAGE,
        "min_cena": MIN_PRICE,
        "max_cena": MAX_PRICE,
        "wykluczone_paliwa": list(EXCLUDED_FUEL_TYPES),
    }


def _empty_row() -> dict[str, Any]:
    return {column: None for column in metadata()["kolumny_wejsciowe_wszystkie"]}


def _to_frame(row: dict[str, Any]) -> pd.DataFrame:
    """Buduje jednowierszową ramkę o typach identycznych z treningowymi.

    Rzutowanie nie jest ozdobą: zły dtype potrafi dać cichą, błędną wycenę zamiast
    wyjątku, bo OneHotEncoder ma handle_unknown='ignore' i niedopasowaną wartość
    koduje wektorem zer.
    """
    columns = metadata()["kolumny_wejsciowe_wszystkie"]
    frame = pd.DataFrame([row], columns=columns)

    for column, dtype in metadata()["dtypes"].items():
        if dtype.startswith("int") and frame[column].isna().any():
            dtype = "float64"
        frame[column] = frame[column].astype(dtype)

    return frame


def build_frame(payload) -> pd.DataFrame:
    """Przekłada obiekt wejściowy API na ramkę oczekiwaną przez pipeline."""
    row = _empty_row()

    row["wiek_auta"] = date.today().year - payload.rok_produkcji
    row["przebieg"] = payload.przebieg
    row["pojemnosc_silnika"] = payload.pojemnosc_silnika
    row["moc_silnika"] = payload.moc_silnika
    row["ilosc_wyposazenia"] = payload.poziom_wyposazenia

    for column in PASSTHROUGH_CATEGORICAL:
        row[column] = getattr(payload, column)

    row["importowany"] = "Tak" if payload.importowany else "Nie"
    for column, enabled in payload.wyposazenie.model_dump().items():
        row[column] = "Tak" if enabled else "Nie"

    return _to_frame(row)


def _round_to_hundreds(value: float) -> int:
    return int(round(value / 100.0) * 100)


def _build_warnings(payload, price: float) -> list[str]:
    """Sygnalizuje wejście poza dziedziną treningu. Predykcja się udała, ale jest
    mniej wiarygodna - to nie jest powód do odrzucenia żądania."""
    warnings: list[str] = []

    if payload.przebieg < MIN_MILEAGE:
        warnings.append(
            f"Model trenowano na pojazdach używanych (przebieg od {MIN_MILEAGE:,} km). "
            "Dla niższego przebiegu wycena może być zaniżona.".replace(",", " ")
        )

    if price < MIN_PRICE or price > MAX_PRICE:
        warnings.append(
            f"Wycena wypada poza zakresem cen zbioru treningowego "
            f"({MIN_PRICE:,} - {MAX_PRICE:,} PLN) i jest mniej wiarygodna.".replace(",", " ")
        )

    return warnings


def predict(payload) -> dict[str, Any]:
    frame = build_frame(payload)
    price = float(_state["model"].predict(frame)[0])

    mape = float(metadata()["test_metrics"]["MAPE"])
    margin = price * mape / 100.0

    return {
        "przewidywana_cena": _round_to_hundreds(price),
        "waluta": "PLN",
        "przedzial": {
            "od": _round_to_hundreds(max(price - margin, 0)),
            "do": _round_to_hundreds(price + margin),
        },
        "model_version": metadata()["train_timestamp"],
        "ostrzezenia": _build_warnings(payload, price),
    }


def model_info() -> dict[str, Any]:
    meta = metadata()
    return {
        "model_name": meta["model_name"],
        "train_timestamp": meta["train_timestamp"],
        "train_shape": list(meta["train_shape"]),
        "liczba_cech_wejsciowych": len(meta["kolumny_wejsciowe_wszystkie"]),
        "metryki_testowe": {
            "MAPE": round(float(meta["test_metrics"]["MAPE"]), 2),
            "MAE": round(float(meta["test_metrics"]["MAE"]), 0),
            "RMSE": round(float(meta["test_metrics"]["RMSE"]), 0),
            "R2": round(float(meta["test_metrics"]["R2"]), 3),
        },
        "wersje_bibliotek": meta["library_versions"],
    }
