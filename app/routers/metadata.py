from fastapi import APIRouter

from app import labels, model_service
from app.schemas import FormOptionsOut, ModelInfoOut

router = APIRouter(prefix="/api/v1", tags=["metadata"])


@router.get("/form-options", response_model=FormOptionsOut)
def form_options() -> FormOptionsOut:
    """Wszystko, co frontend potrzebuje do zbudowania formularza.

    Listy pochodzą z tego samego artefaktu, z którego korzysta predykcja, więc
    formularz nie może zaproponować wartości nieznanej modelowi.
    """
    return FormOptionsOut(
        kategorie=model_service.category_options(),
        etykiety_kategorii=labels.CATEGORY_LABELS,
        etykiety_wartosci=labels.VALUE_LABELS,
        zakresy=model_service.numeric_ranges(),
        ograniczenia=model_service.constraints(),
        wyposazenie=[
            {"nazwa": column, "etykieta": labels.EQUIPMENT_LABELS[column]}
            for column in model_service.EQUIPMENT_FLAGS
        ],
        presety_wyposazenia=labels.EQUIPMENT_PRESETS,
    )


@router.get("/model-info", response_model=ModelInfoOut)
def model_info() -> ModelInfoOut:
    return ModelInfoOut(**model_service.model_info())
