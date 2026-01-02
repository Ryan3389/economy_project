from prefect.variables import Variable

fred_api_key = Variable.get("key")
db = Variable.get("db")


if not db:
    raise RuntimeError("Prefect variable 'db' is not set")

if not fred_api_key:
    raise RuntimeError("Prefect variable 'key' not set")

# import os
# from dotenv import load_dotenv
# from prefect.variables import Variable


# load_dotenv()

# fred_api_key = os.getenv("key")
# db = os.getenv("db")

# if not db:
#     raise RuntimeError("Environment variable 'db' is not set")
