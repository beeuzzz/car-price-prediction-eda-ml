import logging

from fastapi import APIRouter, HTTPException, status

from app import model_service
from app.schemas import CarFeaturesIn, PredictionOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["predict"])


@router.post("/predict", response_model=PredictionOut)
def predict(payload: CarFeaturesIn) -> PredictionOut:
    if not model_service.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded",
        )

    result = model_service.predict(payload)

    logger.info(
        "prediction brand=%s year=%s mileage=%.0f -> %d PLN",
        payload.brand,
        payload.production_year,
        payload.mileage,
        result["predicted_price"],
    )

    return PredictionOut(**result)
