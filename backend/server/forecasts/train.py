from backend.server.forecasts.data import load_features
import joblib
import json
from datetime import datetime, timezone
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import math
from pathlib import Path

df = load_features()

df["cpi_target_1m"] = df["cpi_value"].shift(-1) 
df["cpi_target_3m"] = df["cpi_value"].shift(-3) 
df["cpi_target_6m"] = df["cpi_value"].shift(-6) 

print(df[["date", "cpi_value", "cpi_target_1m", "cpi_target_3m", "cpi_target_6m"]])

df_1m = df.dropna(subset=["cpi_target_1m"])
df_3m = df.dropna(subset=["cpi_target_3m"])
df_6m = df.dropna(subset=["cpi_target_6m"])

rows_with_nan_1m = df_1m[df_1m.isna().any(axis=1)]
rows_with_nan_3m = df_3m[df_3m.isna().any(axis=1)]
rows_with_nan_6m = df_6m[df_6m.isna().any(axis=1)]


df_1m = df_1m.drop(rows_with_nan_1m.index, axis=0)
df_3m = df_3m.drop(rows_with_nan_3m.index, axis=0)
df_6m = df_6m.drop(rows_with_nan_6m.index, axis=0)

X_1m = df_1m.drop(["cpi_target_1m", "cpi_target_3m", "cpi_target_6m", "date"], axis=1)
X_3m = df_3m.drop(["cpi_target_1m", "cpi_target_3m", "cpi_target_6m", "date"], axis=1)
X_6m = df_6m.drop(["cpi_target_1m", "cpi_target_3m", "cpi_target_6m", "date"], axis=1)

y_1m = df_1m["cpi_target_1m"]
y_3m = df_3m["cpi_target_3m"]
y_6m = df_6m["cpi_target_6m"]

feature_columns = X_1m.columns.tolist()
with open("economic_model_features.json", "w") as f:
    json.dump(feature_columns, f, indent=4)

X_1m = X_1m[feature_columns]
X_3m = X_3m[feature_columns]
X_6m = X_6m[feature_columns]

n_1m = len(df_1m)
n_3m = len(df_3m)
n_6m = len(df_6m)

split_idx_1m = int(n_1m * 0.8)
split_idx_3m = int(n_3m * 0.8)
split_idx_6m = int(n_6m * 0.8)

X_train_1m = X_1m[:split_idx_1m]
X_test_1m = X_1m[split_idx_1m:]
y_train_1m = y_1m[:split_idx_1m]
y_test_1m = y_1m[split_idx_1m:]

X_train_3m = X_3m[:split_idx_3m]
X_test_3m = X_3m[split_idx_3m:]
y_train_3m = y_3m[:split_idx_3m]
y_test_3m = y_3m[split_idx_3m:]

X_train_6m = X_6m[:split_idx_6m]
X_test_6m = X_6m[split_idx_6m:]
y_train_6m = y_6m[:split_idx_6m]
y_test_6m = y_6m[split_idx_6m:]

LR_model_1m = LinearRegression()
LR_model_3m = LinearRegression()
LR_model_6m = LinearRegression()

LR_model_1m.fit(X_train_1m, y_train_1m)
LR_model_3m.fit(X_train_3m, y_train_3m)
LR_model_6m.fit(X_train_6m, y_train_6m)

y_pred_1m = LR_model_1m.predict(X_test_1m)
y_pred_3m = LR_model_3m.predict(X_test_3m)
y_pred_6m = LR_model_6m.predict(X_test_6m)


mae_1m = mean_absolute_error(y_test_1m, y_pred_1m)
print("Mean Absolute Error 1 Month Forecasting")
print(mae_1m)

mae_3m = mean_absolute_error(y_test_3m, y_pred_3m)
print("Mean Absolute Error 3 Month Forecasting")
print(mae_3m)

mae_6m = mean_absolute_error(y_test_6m, y_pred_6m)
print("Mean Absolute Error 6 Month Forecasting")
mae_6m


mse_1m = mean_squared_error(y_test_1m, y_pred_1m)
print("Mean Squared Error 3 Month Forecasting")
mse_1m

mse_3m = mean_squared_error(y_test_3m, y_pred_3m)
print("Mean Squared Error 3 Month Forecasting")
mse_3m

mse_6m = mean_squared_error(y_test_6m, y_pred_6m)

print("Mean Squared Error 6 Month Forecasting")
mse_6m


rmse_1m = math.sqrt(mse_1m)
print("Root Mean Squared Error 1 Month Forecasting")
rmse_1m


rmse_3m = math.sqrt(mse_3m)
print("Root Mean Squared Error 3 Month Forecasting")
rmse_3m


rmse_6m = math.sqrt(mse_6m)
print("Root Mean Squared Error 6 Month Forecasting")
rmse_6m



artifacts_dir = Path("artifacts")
if not artifacts_dir.exists():
    artifacts_dir.mkdir(parents=True)

joblib.dump(LR_model_1m, artifacts_dir / "LR_model_1m.pkl")
joblib.dump(LR_model_3m, artifacts_dir / "LR_model_3m.pkl")
joblib.dump(LR_model_6m, artifacts_dir / "LR_model_6m.pkl")


train_dates_1m = df_1m["date"].iloc[:split_idx_1m]
test_dates_1m = df_1m["date"].iloc[split_idx_1m:]

model_meta_data_1m =  {
    "model_name": "LR_1m",
    "target": "cpi_value",
    "horizon_months": 1,
    "version": "v1.0",
    "trained_at": datetime.now(timezone.utc).isoformat(),
    "data": {
        "train_rows": len(X_train_1m),
        "test_rows": len(X_test_1m),
        "train_start_date": str(train_dates_1m.min().date()),
        "train_end_date": str(train_dates_1m.max().date()),
        "test_start_date": str(test_dates_1m.min().date()),
        "test_end_date": str(test_dates_1m.max().date()),
    },
    "metrics": {
        "mae": mae_1m,
        "rmse": rmse_1m
    },
    "artifacts": {
        "model_file": "artifacts/LR_model_1m.pkl",
        "features_file": "artifacts/economic_features.json"
    }
}


train_dates_3m = df_3m["date"].iloc[:split_idx_3m]
test_dates_3m = df_3m["date"].iloc[split_idx_3m:]

model_meta_data_3m =  {
    "model_name": "LR_3m",
    "target": "cpi_value",
    "horizon_months": 3,
    "version": "v1.0",
    "trained_at": datetime.now(timezone.utc).isoformat(),
    "data": {
        "train_rows": len(X_train_3m),
        "test_rows": len(X_test_3m),
        "train_start_date": str(train_dates_3m.min().date()),
        "train_end_date": str(train_dates_3m.max().date()),
        "test_start_date": str(test_dates_3m.min().date()),
        "test_end_date": str(test_dates_3m.max().date())
    },
        "metrics": {
        "mae": mae_3m,
        "rmse": rmse_3m
    },
    "artifacts": {
        "model_file": "artifacts/LR_model_3m.pkl",
        "features_file": "artifacts/economic_features.json"
    }
}


train_dates_6m = df_6m["date"].iloc[:split_idx_6m]
test_dates_6m = df_6m["date"].iloc[split_idx_6m:]

model_meta_data_6m =  {
    "model_name": "LR_6m",
    "target": "cpi_value",
    "horizon_months": 6,
    "version": "v1.0",
    "trained_at": datetime.now(timezone.utc).isoformat(),
    "data": {
        "train_rows": len(X_train_6m),
        "test_rows": len(X_test_6m),
        "train_start_date": str(train_dates_6m.min().date()),
        "train_end_date": str(train_dates_6m.max().date()),
        "test_start_date": str(test_dates_6m.min().date()),
        "test_end_date": str(test_dates_6m.max().date())
    },
        "metrics": {
        "mae": mae_6m,
        "rmse": rmse_6m
    },
    "artifacts": {
        "model_file": "artifacts/LR_model_6m.pkl",
        "features_file": "artifacts/economic_features.json"
    }
}

runs = [model_meta_data_1m, model_meta_data_3m, model_meta_data_6m]

model_meta_data = {
    "project": "economic_forecasting",
    "created_at":  datetime.now(timezone.utc).isoformat(),
    "description":"Baseline linear regression models for CPI forecasting using macroeconomic indicators",
    "runs": runs
}


with open("artifacts/training_metadata.json", "w") as f:
    json.dump(model_meta_data, f, indent=4, default=str)