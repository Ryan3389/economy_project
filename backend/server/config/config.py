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


# db = get_db()
# fred_api_key = get_fred_api_key()



import os
from prefect.variables import Variable

def get_setting(name: str) -> str:
    val = os.getenv(name)
    if val:
        return val

    val = Variable.get(name, default=None)

    # if Prefect ever returns a coroutine, this will catch it immediately
    if hasattr(val, "__await__"):
        raise TypeError(f"Prefect Variable '{name}' returned a coroutine. Use env vars or resolve it inside a task/flow context.")

    if not val:
        raise RuntimeError(f"Missing required setting '{name}' (env var or Prefect Variable).")

    return val

def get_db() -> str:
    return get_setting("db")

def get_fred_api_key() -> str:
    return get_setting("key")
