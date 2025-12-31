from server.db.db import get_connection
import pandas as pd
from server.forecasts.services.model_loader import load_model
from datetime import datetime, timezone
from decimal import Decimal

def economy_forecasts(horizon_months: int):
    dt = datetime.now(timezone.utc) 

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
                df = pd.DataFrame(rows, columns=columns).drop(columns=['date'])

                model = load_model(horizon_months)
                model_prediction = model.predict(df)

                prediction_response = {
                    "horizon_months": horizon_months,
                    "model_prediction": int(model_prediction)
                }
                target_metric = df.columns[0]
                print(type(float(model_prediction)))

                store_model_predictions(dt, f"LR_model_{horizon_months}m", "v1.0", target_metric, horizon_months, Decimal(str(model_prediction.item())))
                # store_model_predictions(dt, f"LR_model_{horizon_months}m", "v1.0", target_metric, horizon_months, Decimal(model_prediction))
                return prediction_response
            
    finally:
        conn.close()


def store_model_predictions(timestamp, model_name, model_version, target_metric, horizon_months, predicted_value):
   insert_pred_sql = """
        INSERT INTO forecast_predictions (run_timestamp, model_name, model_version, target_metric, horizon_months, predicted_value)

        VALUES (%s, %s, %s, %s, %s, %s)
    """
   
   conn = get_connection()

   try: 
       with conn:
           with conn.cursor() as cur:
               cur.execute(insert_pred_sql, (timestamp, model_name, model_version, target_metric, horizon_months, predicted_value))
   finally:
       conn.close()

"""
    1. Open DB Connection
    2. Query lastest row from economy_model_features (not the raw long table)
    3. Build a 1 row DataFrame
    4. Load economic_features/json
    5. Validate NaNs (decide: block or impute)
    6. For each requestied horizon:
        a. Load model file for that horizon
        b. Predict
        c. Create a “prediction row” dict (for DB insert)
    7. Return predictions + run_id
    """
