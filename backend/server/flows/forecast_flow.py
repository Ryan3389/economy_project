from prefect import task, flow, get_run_logger
# from server.forecasts.train_model import run_training_pipeline
from server.forecasts.train_model import run_training_pipeline
# from server.forecasts.data import load_features
from server.forecasts.data import load_features
from server.controllers.forecastControllers import store_model_predictions
from server.db.db import get_connection
from datetime import datetime, timezone
import pandas as pd


@task(retries=3, retry_delay_seconds=10)
def train_all_models():
    logger = get_run_logger()
    logger.info("Starting model training pipeline (horizons=1,3,6)")
    try:
        result = run_training_pipeline(horizons=(1, 3, 6))
        logger.info("Printing results")
        runs = result['runs']
        print(runs[0]['model_name'])
        return result
    except Exception:
        logger.exception("Model training pipeline failed")
        raise


@flow(name="train-forecast-models")
def train_forecast_models_flow():
    result = train_all_models()
    # store_predictions(result)
    return result

train_forecast_models_flow()


