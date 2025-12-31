from pathlib import Path
# import pickle
import joblib

def load_model(horizon_month: int):
    model_path = (
        Path(__file__).resolve().parents[1]
        / "artifacts"
        / f"LR_model_{horizon_month}m.pkl"
    )

    with open(model_path, "rb") as f:
        return joblib.load(f)

# def predict():
#     model = load_model(1)
#     # model.predict(...) goes here

