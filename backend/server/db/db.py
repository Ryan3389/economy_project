import psycopg2
import os
# from backend.server.config.config import db
from backend.server.config.config import get_db
db = get_db()



def get_connection():
     return psycopg2.connect(db)


def init_db():
    create_table = """
    CREATE TABLE IF NOT EXISTS economy_metrics
 (
        series_id VARCHAR(255) NOT NULL,
        metric_name VARCHAR(50) NOT NULL,
        date DATE NOT NULL,
        value DOUBLE PRECISION,
        created_at TIMESTAMP DEFAULT NOW(),
        PRIMARY KEY (series_id, date)
    );
"""
    create_indexes = [
        """
            CREATE INDEX IF NOT EXISTS idx_economy_metric_date
            ON economy_metrics (metric_name, date);
        """,
        """
            CREATE INDEX IF NOT EXISTS idx_economy_date
            ON economy_metrics (date)
        """
    ]

    
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(create_table)
                for sql in create_indexes: 
                    cur.execute(sql)
    finally:
        conn.close()
    print("Table creation executed")







