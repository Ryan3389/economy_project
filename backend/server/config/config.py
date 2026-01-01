import os
from dotenv import load_dotenv

load_dotenv()

fred_api_key = os.getenv("key")
db = os.getenv("db")

