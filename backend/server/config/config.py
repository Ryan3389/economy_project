# backend/server/config/config.py
import os
from prefect.variables import Variable

def get_setting(name: str, required: bool = True) -> str | None:
 
    val = os.getenv(name)
    if val:
        return val

   
    val = Variable.get(name, default=None)

    if required and not val:
        raise RuntimeError(f"Missing required setting '{name}' (env var or Prefect Variable).")

    return val

def get_db() -> str:
    return get_setting("db", required=True)

def get_fred_api_key() -> str:
    return get_setting("key", required=True)



# from prefect.variables import Variable

# fred_api_key = Variable.get("key")
# db = Variable.get("db")


# if not db:
#     raise RuntimeError("Prefect variable 'db' is not set")

# if not fred_api_key:
#     raise RuntimeError("Prefect variable 'key' not set")


