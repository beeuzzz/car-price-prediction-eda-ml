from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app import model_service
from src.config import MAX_CAR_AGE

CURRENT_YEAR = date.today().year
OLDEST_YEAR = CURRENT_YEAR - MAX_CAR_AGE


class Equipment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    leather_upholstery: bool = False
    dealership_serviced: bool = False
    panoramic_roof: bool = False
    led_headlights: bool = False
    led_taillights: bool = False
    first_owner: bool = False
    automatic_ac: bool = False
    rearview_camera: bool = False
    heated_seats: bool = False
    cruise_control: bool = False
    adaptive_cruise_control: bool = False
    traffic_sign_recognition: bool = False
    wireless_charger: bool = False
    android_auto: bool = False


class CarFeaturesIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    brand: str
    production_year: int = Field(ge=OLDEST_YEAR, le=CURRENT_YEAR)
    mileage: float = Field(ge=0, le=1_000_000)

    engine_capacity: float | None = Field(default=None, ge=400, le=8000)
    engine_power: float | None = Field(default=None, ge=30, le=1000)
    gearbox: str | None = None
    fuel_type: str | None = None
    drive: str | None = None
    voivodeship: str | None = None
    body_type: str | None = None
    color: str | None = None
    seller_type: str | None = None

    equipment_level: int | None = Field(default=None, ge=0, le=150)
    imported: bool = False
    equipment: Equipment = Field(default_factory=Equipment)

    @model_validator(mode="after")
    def validate_against_model_categories(self):
        if not model_service.is_ready():
            return self

        problems = []
        for field, allowed in model_service.category_options().items():
            value = getattr(self, field, None)
            if value is not None and value not in allowed:
                problems.append(
                    f"{field}: '{value}' is not a value known to the model "
                    f"(allowed: {', '.join(allowed)})"
                )

        if problems:
            raise ValueError("; ".join(problems))

        return self


class PriceRange(BaseModel):
    low: int
    high: int


class PredictionOut(BaseModel):
    predicted_price: int
    currency: str
    price_range: PriceRange
    model_version: str
    warnings: list[str]


class FormOptionsOut(BaseModel):
    categories: dict[str, list[str]]
    category_labels: dict[str, str]
    value_labels: dict[str, dict[str, str]]
    ranges: dict[str, dict[str, float]]
    constraints: dict[str, object]
    equipment: list[dict[str, str]]
    equipment_presets: list[dict[str, object]]


class ModelInfoOut(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_name: str
    train_timestamp: str
    train_shape: list[int]
    input_feature_count: int
    test_metrics: dict[str, float]
    library_versions: dict[str, str]
