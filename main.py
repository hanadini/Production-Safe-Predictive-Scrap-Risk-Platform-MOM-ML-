from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Production-Safe Predictive Scrap Risk Platform",
    description="FastAPI service for production-safe scrap risk prediction in MOM/MES environments",
    version="1.0.0"
)


class PredictionRequest(BaseModel):
    press_pressure_left: float
    press_pressure_mid: float
    press_pressure_right: float
    press_temperature: float
    line_speed: float
    moisture: float
    shift_id: Optional[str] = None
    product_type: Optional[str] = None

class PredictionResponse(BaseModel):
    scrap_risk: float
    risk_level: str
    recommendation: str
    timestamp: str


@app.get("/")
def root():
    return {
        "service": "Production-Safe Predictive Scrap Risk Platform",
        "status": "running",
        "mode": "safe"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_scrap_risk(request: PredictionRequest):
    avg_pressure = (
        request.press_pressure_left
        + request.press_pressure_mid
        + request.press_pressure_right
    ) / 3

    risk_score = 0.0

    if avg_pressure < 150:
        risk_score += 0.30
    if request.press_temperature < 160:
        risk_score += 0.20
    if request.line_speed > 80:
        risk_score += 0.25
    if request.moisture > 9:
        risk_score += 0.25

    risk_score = min(risk_score, 1.0)

    if risk_score < 0.30:
        risk_level = "LOW"
        recommendation = "No action required. Continue monitoring."
    elif risk_score < 0.60:
        risk_level = "MEDIUM"
        recommendation = "Increase monitoring and verify process parameters."
    else:
        risk_level = "HIGH"
        recommendation = "Trigger operator review and apply fail-safe checks before action."

    return PredictionResponse(
        scrap_risk=round(risk_score, 3),
        risk_level=risk_level,
        recommendation=recommendation,
        timestamp=datetime.utcnow().isoformat()
    )