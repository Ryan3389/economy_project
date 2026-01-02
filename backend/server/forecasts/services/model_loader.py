from pathlib import Path

import joblib

from pathlib import Path
import joblib

def load_model(model_name: str, horizon_months:int):
    model_path = Path(__file__).resolve().parents[1] / "artifacts" / f"{model_name}.pkl"

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found at {model_path}. Run forecast-flow first to create it."
        )

    return joblib.load(model_path)



# from pathlib import Path

# import joblib

# def load_model(horizon_month: int):
#     model_path = (
#         Path(__file__).resolve().parents[1]
#         / "artifacts"
#         / f"LR_model_{horizon_month}m.pkl"
#     )

#     with open(model_path, "rb") as f:
#         return joblib.load(f)



