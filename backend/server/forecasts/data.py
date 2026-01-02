from backend.server.db.db import get_connection
import pandas as pd
import numpy as np
import datetime
from prefect import task

@task(retries=3, retry_delay_seconds=10)
def load_features():
    conn = get_connection()

    sql_query = """
    
   SELECT * FROM economic_model_features
        """
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql_query)
                rows = cur.fetchall()

               
                data_cols = []
                for col in cur.description: 
                    data_cols.append(col[0])
                
                df = pd.DataFrame(rows, columns=data_cols)

                df["date"] = pd.to_datetime(df["date"])
                df.sort_values(by='date', ascending=True, inplace=True)

                return df
    finally:
        conn.close()





