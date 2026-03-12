from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
    prediction_source: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str = datetime.utcnow().isoformat()