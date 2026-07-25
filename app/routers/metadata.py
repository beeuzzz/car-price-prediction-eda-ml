from fastapi import APIRouter

from app import labels, model_service
from app.schemas import FormOptionsOut, ModelInfoOut

router = APIRouter(prefix="/api/v1", tags=["metadata"])


@router.get("/form-options", response_model=FormOptionsOut)
def form_options() -> FormOptionsOut:
    return FormOptionsOut(
        categories=model_service.category_options(),
        category_labels=labels.CATEGORY_LABELS,
        value_labels=labels.VALUE_LABELS,
        ranges=model_service.numeric_ranges(),
        constraints=model_service.constraints(),
        equipment=[
            {"name": field, "label": labels.EQUIPMENT_LABELS[field]}
            for field in model_service.EQUIPMENT_FIELDS
        ],
        equipment_presets=labels.EQUIPMENT_PRESETS,
    )


@router.get("/model-info", response_model=ModelInfoOut)
def model_info() -> ModelInfoOut:
    return ModelInfoOut(**model_service.model_info())
