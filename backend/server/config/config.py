
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


db = get_db()
fred_api_key = get_fred_api_key()

# import os
# from prefect.variables import Variable

# def get_setting(name: str, required: bool = True) -> str | None:
#     # Prefer env if present (works locally + on Prefect if you later use env)
#     val = os.getenv(name)
#     if val:
#         return val

#     # Otherwise Prefect Variable (sync)
#     val = Variable.get(name, default=None)

#     if required and not val:
#         raise RuntimeError(f"Missing required setting '{name}' (env var or Prefect Variable).")

#     return val

# db = get_setting("db", required=True)
# fred_api_key = get_setting("key", required=True)

# # backend/server/config/config.py
# import os
# from prefect.variables import Variable

# def get_setting(name: str, required: bool = True) -> str | None:
 
#     val = os.getenv(name)
#     if val:
#         return val

   
#     val = Variable.get(name, default=None)

#     if required and not val:
#         raise RuntimeError(f"Missing required setting '{name}' (env var or Prefect Variable).")

#     return val

# def get_db() -> str:
#     return get_setting("db", required=True)

# def get_fred_api_key() -> str:
#     return get_setting("key", required=True)




