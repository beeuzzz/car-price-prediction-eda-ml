import logging
from datetime import date
from typing import Any

import joblib
import pandas as pd

from app.settings import settings
from src.config import (
    EXCLUDED_FUEL_TYPES,
    MAX_CAR_AGE,
    MAX_PRICE,
    MIN_MILEAGE,
    MIN_PRICE,
)

logger = logging.getLogger(__name__)

INPUT_COLUMNS_KEY = "kolumny_wejsciowe_wszystkie"
COLUMN_CATEGORIES_KEY = "kategorie_kolumn"

REQUIRED_METADATA_KEYS = (
    INPUT_COLUMNS_KEY,
    COLUMN_CATEGORIES_KEY,
    "dtypes",
    "test_metrics",
    "train_timestamp",
)

CAR_AGE_COLUMN = "wiek_auta"
MILEAGE_COLUMN = "przebieg"
ENGINE_CAPACITY_COLUMN = "pojemnosc_silnika"
ENGINE_POWER_COLUMN = "moc_silnika"
EQUIPMENT_LEVEL_COLUMN = "ilosc_wyposazenia"
IMPORTED_COLUMN = "importowany"

CATEGORICAL_FIELDS = {
    "brand": "marka",
    "gearbox": "skrzynia_biegow",
    "fuel_type": "paliwo",
    "drive": "naped",
    "voivodeship": "wojewodztwo",
    "body_type": "nadwozie",
    "color": "kolor",
    "seller_type": "typ_sprzedawcy",
}

EQUIPMENT_FIELDS = {
    "leather_upholstery": "skorzana_tapicerka",
    "dealership_serviced": "serwis_aso",
    "panoramic_roof": "dach_panoramiczny",
    "led_headlights": "swiatla_led",
    "first_owner": "pierwszy_wlasciciel",
    "automatic_ac": "klimatyzacja_automatyczna",
    "rearview_camera": "kamera_cofania",
    "heated_seats": "podgrzewane_fotele",
    "cruise_control": "tempomat",
    "adaptive_cruise_control": "aktywny_tempomat",
    "traffic_sign_recognition": "czytanie_znakow",
    "wireless_charger": "ladowarka_indukcyjna",
    "led_taillights": "swiatla_tylne_led",
    "android_auto": "android_auto",
}

YES = "Tak"
NO = "Nie"

_state: dict[str, Any] = {}


def load() -> None:
    logger.info("Loading artifacts from %s", settings.model_path.parent)

    for path in (settings.model_path, settings.metadata_path):
        if not path.exists():
            raise RuntimeError(
                f"Missing artifact {path}. Train the model with: python run_pipeline.py"
            )

    _state["model"] = joblib.load(settings.model_path)
    _state["metadata"] = joblib.load(settings.metadata_path)

    missing = [key for key in REQUIRED_METADATA_KEYS if key not in _state["metadata"]]
    if missing:
        _state.clear()
        raise RuntimeError(
            f"Model metadata does not contain the keys {missing}. "
            "The artifact comes from an older version of the code - retrain it: "
            "python run_pipeline.py"
        )

    logger.info(
        "Model ready: %s, %d input features, trained %s",
        _state["metadata"]["model_name"],
        len(_state["metadata"][INPUT_COLUMNS_KEY]),
        _state["metadata"]["train_timestamp"],
    )


def unload() -> None:
    _state.clear()


def is_ready() -> bool:
    return "model" in _state and "metadata" in _state


def metadata() -> dict[str, Any]:
    if not is_ready():
        raise RuntimeError("Model is not loaded")
    return _state["metadata"]


def warmup() -> None:
    row = _empty_row()
    row.update({CATEGORICAL_FIELDS["brand"]: "Audi", CAR_AGE_COLUMN: 7, MILEAGE_COLUMN: 120000.0})
    price = float(_state["model"].predict(_to_frame(row))[0])
    logger.info("Warmup finished (control prediction: %.0f PLN)", price)


def category_options() -> dict[str, list[str]]:
    categories = metadata()[COLUMN_CATEGORIES_KEY]
    options: dict[str, list[str]] = {}

    for field, column in CATEGORICAL_FIELDS.items():
        values = [value for value in categories.get(column, []) if isinstance(value, str)]

        if field == "fuel_type":
            values = [value for value in values if value not in EXCLUDED_FUEL_TYPES]

        options[field] = sorted(values)

    return options


def numeric_ranges() -> dict[str, dict[str, float]]:
    from app.schemas import CURRENT_YEAR, OLDEST_YEAR

    return {
        "production_year": {"min": OLDEST_YEAR, "max": CURRENT_YEAR},
        "mileage": {"min": 0, "max": 1_000_000},
        "engine_capacity": {"min": 400, "max": 8000},
        "engine_power": {"min": 30, "max": 1000},
        "equipment_level": {"min": 0, "max": 150},
    }


def constraints() -> dict[str, Any]:
    from app.schemas import CURRENT_YEAR, OLDEST_YEAR

    return {
        "min_year": OLDEST_YEAR,
        "max_year": CURRENT_YEAR,
        "max_car_age": MAX_CAR_AGE,
        "min_mileage": MIN_MILEAGE,
        "min_price": MIN_PRICE,
        "max_price": MAX_PRICE,
        "excluded_fuel_types": list(EXCLUDED_FUEL_TYPES),
    }


def _empty_row() -> dict[str, Any]:
    return {column: None for column in metadata()[INPUT_COLUMNS_KEY]}


def _to_frame(row: dict[str, Any]) -> pd.DataFrame:
    columns = metadata()[INPUT_COLUMNS_KEY]
    frame = pd.DataFrame([row], columns=columns)

    for column, dtype in metadata()["dtypes"].items():
        if dtype.startswith("int") and frame[column].isna().any():
            dtype = "float64"
        frame[column] = frame[column].astype(dtype)

    return frame


def build_frame(payload) -> pd.DataFrame:
    row = _empty_row()

    row[CAR_AGE_COLUMN] = date.today().year - payload.production_year
    row[MILEAGE_COLUMN] = payload.mileage
    row[ENGINE_CAPACITY_COLUMN] = payload.engine_capacity
    row[ENGINE_POWER_COLUMN] = payload.engine_power
    row[EQUIPMENT_LEVEL_COLUMN] = payload.equipment_level

    for field, column in CATEGORICAL_FIELDS.items():
        row[column] = getattr(payload, field)

    row[IMPORTED_COLUMN] = YES if payload.imported else NO
    for field, enabled in payload.equipment.model_dump().items():
        row[EQUIPMENT_FIELDS[field]] = YES if enabled else NO

    return _to_frame(row)


def _round_to_hundreds(value: float) -> int:
    return int(round(value / 100.0) * 100)


def _build_warnings(payload, price: float) -> list[str]:
    warnings: list[str] = []

    if payload.mileage < MIN_MILEAGE:
        warnings.append(
            f"The model was trained on used vehicles (mileage from {MIN_MILEAGE:,} km). "
            "For a lower mileage the valuation may be understated."
        )

    if price < MIN_PRICE or price > MAX_PRICE:
        warnings.append(
            f"The valuation falls outside the price range of the training set "
            f"({MIN_PRICE:,} - {MAX_PRICE:,} PLN) and is less reliable."
        )

    return warnings


def predict(payload) -> dict[str, Any]:
    frame = build_frame(payload)
    price = float(_state["model"].predict(frame)[0])

    mape = float(metadata()["test_metrics"]["MAPE"])
    margin = price * mape / 100.0

    return {
        "predicted_price": _round_to_hundreds(price),
        "currency": "PLN",
        "price_range": {
            "low": _round_to_hundreds(max(price - margin, 0)),
            "high": _round_to_hundreds(price + margin),
        },
        "model_version": metadata()["train_timestamp"],
        "warnings": _build_warnings(payload, price),
    }


def model_info() -> dict[str, Any]:
    meta = metadata()
    return {
        "model_name": meta["model_name"],
        "train_timestamp": meta["train_timestamp"],
        "train_shape": list(meta["train_shape"]),
        "input_feature_count": len(meta[INPUT_COLUMNS_KEY]),
        "test_metrics": {
            "MAPE": round(float(meta["test_metrics"]["MAPE"]), 2),
            "MAE": round(float(meta["test_metrics"]["MAE"]), 0),
            "RMSE": round(float(meta["test_metrics"]["RMSE"]), 0),
            "R2": round(float(meta["test_metrics"]["R2"]), 3),
        },
        "library_versions": meta["library_versions"],
    }
