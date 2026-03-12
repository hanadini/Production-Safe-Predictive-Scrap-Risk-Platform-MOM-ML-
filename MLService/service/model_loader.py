import json
from pathlib import Path

try:
    import joblib
except ImportError:
    joblib = None

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "scrap_risk_model.pkl"
FEATURES_PATH = ARTIFACTS_DIR / "feature_columns.json"

DEFAULT_FEATURE_COLUMNS = [
    "press_pressure_left",
    "press_pressure_mid",
    "press_pressure_right",
    "press_temperature",
    "line_speed",
    "moisture"
]

_cached_model = None
_cached_features = None


def get_feature_columns():
    global _cached_features

    if _cached_features is not None:
        return _cached_features

    if FEATURES_PATH.exists():
        with open(FEATURES_PATH, "r", encoding="utf-8") as file:
            _cached_features = json.load(file)
            return _cached_features

    _cached_features = DEFAULT_FEATURE_COLUMNS
    return _cached_features


def get_model():
    global _cached_model

    if _cached_model is not None:
        return _cached_model

    if MODEL_PATH.exists() and joblib is not None:
        _cached_model = joblib.load(MODEL_PATH)
        return _cached_model

    return None