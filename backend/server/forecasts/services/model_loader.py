from pathlib import Path

import joblib

def load_model(horizon_month: int):
    model_path = (
        Path(__file__).resolve().parents[1]
        / "artifacts"
        / f"LR_model_{horizon_month}m.pkl"
    )

    with open(model_path, "rb") as f:
        return joblib.load(f)



