from fastapi import APIRouter, HTTPException
from MLService.models.schemas import PredictionRequest, PredictionResponse, HealthResponse
from MLService.services.prediction_service import calculate_scrap_risk

router = APIRouter()


@router.get("/")
def root():
    return {
        "service": "Production-Safe Predictive Scrap Risk Platform",
        "status": "running",
        "mode": "safe"
    }


@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        service="MLService"
    )


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    try:
        result = calculate_scrap_risk(request)
        return PredictionResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(exc)}")