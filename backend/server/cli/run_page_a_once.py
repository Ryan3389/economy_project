from backend.server.db.db import init_db
from backend.server.etl.page_a_etl import run_page_a_etl
if __name__ == "__main__":
    init_db()
    run_page_a_etl()
    print("Page A ETL complete")