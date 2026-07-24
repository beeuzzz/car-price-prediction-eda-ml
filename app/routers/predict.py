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
            detail="Model nie jest załadowany",
        )

    result = model_service.predict(payload)

    logger.info(
        "predykcja marka=%s rocznik=%s przebieg=%.0f -> %d PLN",
        payload.marka,
        payload.rok_produkcji,
        payload.przebieg,
        result["przewidywana_cena"],
    )

    return PredictionOut(**result)
