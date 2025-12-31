import requests
from prefect import task

from server.config.config import fred_api_key
# from config.config import fred_api_key

base_url = "https://api.stlouisfed.org/fred"

# This function takes in the parameters I need to make my api requests. These will go into the url later on
@task(retries=3, retry_delay_seconds=10)
def get_observations(series_id: str, observation_start: str | None = None):
    params = {
        "series_id": series_id,
        "api_key": fred_api_key,
        "file_type": "json",
    }
    if observation_start:
        params["observation_start"] = observation_start

    response = requests.get(f"{base_url}/series/observations", params=params)
    response.raise_for_status()
    data = response.json()
    return data["observations"]
