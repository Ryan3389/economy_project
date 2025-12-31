import os
from dotenv import load_dotenv

load_dotenv()

fred_api_key = os.getenv("API_KEY")
db_dsn = os.getenv("DB_DSN")

