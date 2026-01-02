import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=ENV_PATH)
print(ENV_PATH)
fred_api_key = os.getenv("key")
db = os.getenv("db")



