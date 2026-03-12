from datetime import datetime

from MLService.services.model_loader import get_model, get_feature_columns


def _build_feature_row(request):
    return {
        "press_pressure_left": request.press_pressure_left,
        "press_pressure_mid": request.press_pressure_mid,
        "press_pressure_right": request.press_pressure_right,
        "press_temperature": request.press_temperature,
        "line_speed": request.line_speed,
        "moisture": request.moisture
    }


def _rule_based_fallback(request):
    avg_pressure = (
        request.press_pressure_left +
        request.press_pressure_mid +
        request.press_pressure_right
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

    return min(risk_score, 1.0)


def _classify_risk(risk_score: float):
    if risk_score < 0.30:
        return "LOW", "Process stable. Continue monitoring."
    elif risk_score < 0.60:
        return "MEDIUM", "Increase monitoring and verify process parameters."
    else:
        return "HIGH", "Trigger operator review and apply fail-safe checks before action."


def calculate_scrap_risk(request):
    model = get_model()
    feature_columns = get_feature_columns()
    feature_row = _build_feature_row(request)

    prediction_source = "rule_based_fallback"

    if model is not None:
        try:
            import pandas as pd

            input_row = {col: feature_row[col] for col in feature_columns}
            input_df = pd.DataFrame([input_row])

            if hasattr(model, "predict_proba"):
                risk_score = float(model.predict_proba(input_df)[0][1])
            else:
                risk_score = float(model.predict(input_df)[0])

            risk_score = max(0.0, min(risk_score, 1.0))
            prediction_source = "trained_model"
        except Exception:
            risk_score = _rule_based_fallback(request)
    else:
        risk_score = _rule_based_fallback(request)

    risk_score = round(risk_score, 3)
    risk_level, recommendation = _classify_risk(risk_score)

    return {
        "scrap_risk": risk_score,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "prediction_source": prediction_source,
        "timestamp": datetime.utcnow().isoformat()
    }