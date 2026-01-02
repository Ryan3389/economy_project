# import os
# from pathlib import Path
# from dotenv import load_dotenv


# ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
# load_dotenv(dotenv_path=ENV_PATH)
# fred_api_key = os.getenv("key")
# db = os.getenv("db")


import os
from dotenv import load_dotenv


load_dotenv()

fred_api_key = os.getenv("key")
db = os.getenv("db")

if not db:
    raise RuntimeError("Environment variable 'db' is not set")
