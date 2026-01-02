from prefect import task, flow, get_run_logger
from backend.server.db.db import get_connection
import pandas as pd
from backend.server.forecasts.services.model_loader import load_model
from datetime import datetime, timezone

@task(retries=3, retry_delay_seconds=10)
def query_data():
    econ_sql_query = """
        SELECT * FROM economic_model_features
        WHERE
            cpi_value IS NOT NULL
            AND interest_value IS NOT NULL
            AND unemployment_value IS NOT NULL
            ORDER BY date DESC
        LIMIT 1;

        """
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(econ_sql_query)
                rows = cur.fetchall()

                columns = [desc[0] for desc in cur.description]
                df = pd.DataFrame(rows, columns=columns).drop(columns=["date"])
                # df = pd.DataFrame(rows, columns=columns).drop(columns=['date'])
                return df
    finally:
        conn.close()

@task(retries=3, retry_delay_seconds=10)
def make_prediction(horizon=[1,3,6]):
    df = query_data()
    predictions = []
    for m in horizon:
        # model = load_model(f"LR_model_{m}m.",m)
        model = load_model(m)
        model_prediction = model.predict(df)
        predictions.append(model_prediction)
    return predictions

    

# make_prediction()

@task(retries=3, retry_delay_seconds=10)
def store_predictions(horizon=[1,3,6]):
    timestamp = datetime.now(timezone.utc)
    
    predictions = make_prediction(horizon)
    insert_pred_sql = """
    INSERT INTO forecast_batch_predictions(run_timestamp, model_name, model_version, target_metric, horizon_months, predicted_value)

    VALUES (%s, %s, %s, %s, %s, %s)
    """
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
               for i, m in enumerate(horizon):
                   model_name = f"LR_{m}m"
                   model_version = "v1.0"
                   target_metric = "cpi_value"
                   
                   predicted_value = float(predictions[i].ravel()[0])
                   cur.execute(
                        insert_pred_sql,
                        (timestamp, model_name, model_version, target_metric, m, predicted_value)
                    )

    finally:
        conn.close()

@flow(name="batch-predict-flow")
def run_predict_flow():
    store_predictions([1, 3, 6])


if __name__ == "__main__":
    run_predict_flow()
  