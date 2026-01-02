import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
print(ENV_PATH)
load_dotenv(dotenv_path=ENV_PATH)

fred_api_key = os.getenv("key")
db = os.getenv("db")
# print(db)


