from server.db.db import get_connection
from server.etl.fred_client import get_observations
from prefect import task, flow, get_run_logger
# from db.db import get_connection
# from etl.fred_client import get_observations
# from prefect import task, flow, get_run_logger

insert_query = """
    INSERT INTO economy_metrics (series_id, metric_name, date, value)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (series_id, date)
    DO UPDATE SET value = EXCLUDED.value;
"""

def save_observations(series_id, metric_name, date, value):
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(insert_query, (series_id, metric_name, date, value))
    finally: 
        conn.close()




series_ids = {
    "Inflation(cpi)": "CANCPIALLMINMEI",
    "Unemployment_Rate": "LRUNTTTTCAM156S",
    "Interest_Rates": "IRSTCB01CAM156N"
}



def get_latest_date(metric_name):
    latest_date_query = """
        SELECT MAX(date)
        FROM economy_metrics
        WHERE metric_name = %s;
    """
    conn = get_connection()

    try: 
        with conn:
            with conn.cursor() as cur:
                cur.execute(latest_date_query, (metric_name,))
                latest_date = cur.fetchone()
                if latest_date[0] is None:
                    return None
                else:
                    return latest_date[0]
    finally:
        conn.close()

@task(retries=2, retry_delay_seconds=10)
def fetch_and_store_metrics(metric_name: str):
    logger = get_run_logger()
    latest_date = get_latest_date(metric_name)
    series_id = series_ids[metric_name]
    observations = get_observations(series_id, observation_start=latest_date)

    if not observations:
        # print(f"No observations found fr series_id={series_id}, metric={metric_name}")
        logger.warning(f"No observations found fr series_id={series_id}, metric={metric_name}")
        return 0
    
    inserted = 0

    for o in observations:
        if o["value"] == ".":
            continue

        date_str = o["date"]
        value = float(o["value"])
        save_observations(series_id, metric_name, date_str, value)
        inserted += 1
    logger.info(f"Stored {inserted} rows for metric={metric_name} series_id={series_id}")
    return inserted


def start_pipeline(flow_name: str):
    conn = get_connection()
    status = "running"

    insert_flow_sql = """
        INSERT INTO pipeline_runs (flow_name, started_at, status)
        VALUES (%s, NOW(), %s)
        RETURNING run_id;
    """
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(insert_flow_sql, (flow_name, status))
                run_id = cur.fetchone()[0]
                return run_id
    finally:
        conn.close()

def finish_pipeline(
        run_id, 
        status: str,
        rows_upserted: int, 
        error_message: str | None = None
        ):
    conn = get_connection()

    update_pipeline_sql = """
        UPDATE pipeline_runs 
        SET 
        finished_at = NOW(),
        rows_upserted = %s, 
        status = %s, 
        error_message = %s
        WHERE run_id = %s;
"""
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(update_pipeline_sql, (rows_upserted, status, error_message, run_id))
    finally:
        conn.close()


@flow
def run_page_a_etl():
    flow_name = "page_a_etl"

    run_id = start_pipeline(flow_name)

    total_rows = 0
    try:
        for metric_name in ["Inflation(cpi)", "Unemployment_Rate", "Interest_Rates"]:
            rows = fetch_and_store_metrics(metric_name)
            total_rows += rows

            finish_pipeline(run_id, "success", total_rows)
    except Exception as e:
        finish_pipeline(run_id, "failed", total_rows, str(e))
# @flow
# def run_page_a_etl():
#     for metric_name in ["Inflation(cpi)", "Unemployment_Rate", "Interest_Rates"]:
#         fetch_and_store_metrics(metric_name)

