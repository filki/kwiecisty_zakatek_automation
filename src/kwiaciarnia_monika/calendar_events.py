import requests
from bs4 import BeautifulSoup
from datetime import date
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_namedays_message(name_day_date: Optional[date] = None) -> str:
    """
    Returns today's name days
    Args:
        date (date): Date to get name days for

    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    logger.info(f"Fetching name days for {name_day_date}")
    url = "https://www.kalbi.pl/kalendarz-imienin"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching name days: {e}")
        return "Nie znaleziono informacji o imieninach na ten dzień."
    soup = BeautifulSoup(response.text, "html.parser")
    name_days = soup.find_all("p", itemprop="text")
    name_list = [name_day.text.replace("\xa0", " ") for name_day in name_days]
    if not name_list:
        logger.error("No name days found for the given date")
        return "Nie znaleziono informacji o imieninach na ten dzień."
    logger.info(f"Name days found: {name_list[0]}")
    return name_list[0]
