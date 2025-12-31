from fastapi import Request
from backend.server.db.db import get_connection
# from db.db import get_connection
from datetime import date


def get_economy_summary():
    econ_sum_sql = """
        SELECT metric_name, as_of_date, latest_value, mom_pct_change, yoy_pct_change, trend_direction, summary
        FROM economic_signals
        ORDER BY metric_name;
    """
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(econ_sum_sql)
                rows = cur.fetchall()

                econ_metrics = []

                for row in rows: 
                    econ_metrics.append ({
                        "metric_name": row[0],
                        "as_of_date": row[1],
                        "latest_value": row[2],
                        "mom_pct_change": row[3],
                        "yoy_pct_change": row[4],
                        "trend_direction": row[5],
                        "summary": row[6]
                    })
                return econ_metrics
    finally:
        conn.close()


def get_metric_trends(slug: str, limit: int = 60):
    METRIC_MAP = {
        "cpi": "Inflation(cpi)",
        "unemployment": "Unemployment_Rate",
        "interest_rates": "Interest_Rates"
    }

    if slug not in METRIC_MAP:
        raise ValueError("Input must be cpi, unemployment, or interest_rates")

    db_metric_name = METRIC_MAP[slug]

    econ_trends_sql = """
        SELECT date, value, rolling_3m_avg, rolling_12m_avg
        FROM macro_features_monthly
        WHERE metric_name = %s
        ORDER BY date DESC
        LIMIT %s;
    """

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(econ_trends_sql, (db_metric_name, limit))
                rows = cur.fetchall()

                econ_trends_data = []
                for row in rows:
                    econ_trends_data.append({
                        "date": row[0],
                        "value": row[1],
                        "rolling_3m_avg": row[2],
                        "rolling_12m_avg": row[3],
                    })

                econ_trends_data.reverse()

                return {
                    "metric": slug,
                    "data": econ_trends_data
                }
    finally:
        conn.close()



# from datetime import date
# from db.db import get_connection

def get_economy_insights():
    econ_insights_sql = """
        SELECT 
            metric_name,
            trend_direction,
            latest_value,
            mom_pct_change,
            yoy_pct_change,
            as_of_date
        FROM economic_signals
        WHERE metric_name IN (
            'Inflation(cpi)',
            'Interest_Rates',
            'Unemployment_Rate'
        );
    """

 
    REVERSE_METRIC_MAP = {
        "Inflation(cpi)": "cpi",
        "Interest_Rates": "interest_rates",
        "Unemployment_Rate": "unemployment"
    }

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(econ_insights_sql)
                rows = cur.fetchall()

              
                signals = {}

                for row in rows:
                    metric_name = row[0]
                    trend_direction = row[1]
                    latest_value = row[2]
                    mom_pct_change = row[3]
                    yoy_pct_change = row[4]
                    as_of_date = row[5]

                    slug = REVERSE_METRIC_MAP[metric_name]

                    signals[slug] = {
                        "trend_direction": trend_direction,
                        "latest_value": latest_value,
                        "mom_pct_change": mom_pct_change,
                        "yoy_pct_change": yoy_pct_change,
                        "as_of_date": as_of_date
                    }

            
                cpi = signals["cpi"]
                rates = signals["interest_rates"]
                unemp = signals["unemployment"]

                if cpi["trend_direction"] == "rising" and rates["trend_direction"] == "rising":
                    headline = "Rising inflation and interest rates are increasing borrowing pressure"
                    explanation = (
                        "Inflation continues to rise while interest rates remain elevated, "
                        "suggesting tighter monetary conditions and increased borrowing costs "
                        "despite relatively stable employment."
                    )
                elif cpi["trend_direction"] == "falling" and unemp["trend_direction"] == "rising":
                    headline = "Cooling inflation amid rising unemployment signals economic slowdown risk"
                    explanation = (
                        "Inflation pressures are easing, but rising unemployment may indicate "
                        "weakening economic conditions."
                    )
                else:
                    headline = "Economic indicators show mixed signals"
                    explanation = (
                        "Recent data presents a mixed outlook, with no clear dominant trend "
                        "across inflation, employment, and interest rates."
                    )

              
                as_of_date = max(
                    cpi["as_of_date"],
                    rates["as_of_date"],
                    unemp["as_of_date"]
                )

            
                return {
                    "headline": headline,
                    "explanation": explanation,
                    "as_of_date": as_of_date
                }

    finally:
        conn.close()


