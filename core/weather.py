"""
Weather operations
"""
import logging
import requests_cache
from retry_requests import retry
import openmeteo_requests


logger = logging.getLogger(__name__)

def get_weather():
    """
    Gets the current temperature from Open-Meteo API.
    
    Returns:
        float: Current temperature.

    Raise:
        requests.exceptions.RequestException: If the request to the Open-Meteo API fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Getting weather data")
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    logger.info("Successfully created cache session")
    openmeteo = openmeteo_requests.Client(session = retry_session)
    logger.info("Successfully created openmeteo client")
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	"latitude": 52.2234,
	"longitude": 18.2512,
	"current": "temperature_2m",
	"forecast_days": 1,
    }
    try:
        responses = openmeteo.weather_api(url, params = params)
        logger.info("Successfully retrieved weather data")
    except Exception as e:
        logger.error(f"Error retrieving weather data: {e}")
        return None

    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    logger.info("Successfully retrieved current temperature")
    rounded_cur_temp = round(current_temperature_2m,2)
    return rounded_cur_temp