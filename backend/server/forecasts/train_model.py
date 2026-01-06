from backend.server.forecasts.data import load_features
import json
import math
from pathlib import Path
from datetime import datetime, timezone

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from prefect import task, flow, get_run_logger



def make_targets(df, horizon: int):
    df[f"cpi_target_{horizon}m"] = df["cpi_value"].shift(-horizon)
    return df


def build_training_frame(df, horizon):
    target_col = f"cpi_target_{horizon}m"

    temp_df = df.dropna(subset=[target_col])

    cleaned_df = temp_df.dropna()

    return cleaned_df



def time_split(X, y, date, horizon, df, train_ratio=0.8):
    target_col = f"cpi_target_{horizon}m"

    # other_targets = [col for col in df.columns if "cpi_target_" in col and col != target_col]
    target_cols = [col for col in df.columns if col.startswith("cpi_target_")]

   
    date_col = date if date else "date"

    cols_to_drop = target_cols + [date_col]

    # cols_to_drop = other_targets + [date_col]

    X = df.drop(columns=cols_to_drop)
    y = df[target_col]

    split_idx = int(len(X) * train_ratio)

    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    return X_train, X_test, y_train, y_test



def train_and_eval_linear_model(X_train, y_train, X_test, y_test, horizon):
    model = LinearRegression()
    ridge_model = Ridge(alpha=1.0)

    model.fit(X_train, y_train)
    ridge_model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred_ridge = ridge_model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = math.sqrt(mse)
    
    ridge_mae = mean_absolute_error(y_test, y_pred_ridge)
    ridge_mse = mean_squared_error(y_test, y_pred_ridge)
    ridge_rmse = math.sqrt(ridge_mse)

    metrics = {
        "lr": {"mae": mae, "mse": mse, "rmse": rmse},
        "ridge": {"alpha": 1.0, "mae": ridge_mae, "mse": ridge_mse, "rmse": ridge_rmse},
    }
    # metrics = {
    #            "mae": mae, 
    #            "ridge_mae": ridge_mae,
    #            "mse": mse, 
    #            "ridge_mse": ridge_mse,
    #            "rmse": rmse,
    #            "ridge_rmse": ridge_rmse
    #            }
    return model,ridge_model, metrics



def train_one_horizon(df: pd.DataFrame, horizon: int, artifacts_dir: Path, date_col: str = "date"):
  
    df_h = build_training_frame(df, horizon)

    X_train, X_test, y_train, y_test = time_split(
        X=None,
        y=None,
        date=date_col,
        horizon=horizon,
        df=df_h,
        train_ratio=0.8,
    )

    model, ridge_model, metrics = train_and_eval_linear_model(X_train, y_train, X_test, y_test, horizon)


    model_path = artifacts_dir / f"LR_model_{horizon}m.pkl"
    joblib.dump(model, model_path)

    ridge_model_path = artifacts_dir / f"ridge_model_{horizon}m.pkl"
    joblib.dump(ridge_model, ridge_model_path)

  

   
    meta = {
        "model_name": f"LR_{horizon}m",
        "model_type": "linear_regression",
        "target": "cpi_value",
        "horizon_months": horizon,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics["lr"],
        "artifacts": {"model_file": str(model_path).replace("\\", "/")},
        "data": {
            "train_rows": len(X_train),
            "test_rows": len(X_test),
            "feature_count": X_train.shape[1],
        },
    }
    ridge_meta  = {
        "model_name": f"ridge_{horizon}m",
        "model_type": "ridge",
        "alpha": 1.0,
        "target": "cpi_value",
        "horizon_months": horizon,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics["ridge"],
        "artifacts": {"model_file": str(ridge_model_path).replace("\\", "/")},
        "data": {
            "train_rows": len(X_train),
            "test_rows": len(X_test),
            "feature_count": X_train.shape[1],
        },
    }

   

    return meta, ridge_meta


def run_training_pipeline(horizons=(1, 3, 6)):
    df = load_features()

   
    df = df.copy()
    for h in horizons:
        df = make_targets(df, h)

    ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    # artifacts_dir = Path("artifacts")
    # artifacts_dir.mkdir(parents=True, exist_ok=True)

    runs = []
    for h in horizons:
        run_meta = train_one_horizon(df, h, ARTIFACTS_DIR, date_col="date")
        runs.append(run_meta)

    training_metadata = {
        "project": "economic_forecasting",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "description": "Baseline linear regression models for CPI forecasting using macroeconomic indicators",
        "runs": runs,
    }

    with open(ARTIFACTS_DIR / "training_metadata.json", "w") as f:
        json.dump(training_metadata, f, indent=4)

    return training_metadata



if __name__ == "__main__":
    run_training_pipeline()


