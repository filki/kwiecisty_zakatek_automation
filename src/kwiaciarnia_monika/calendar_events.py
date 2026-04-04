"""
Calendar events operations
"""

import requests
from bs4 import BeautifulSoup


def get_name_days():
    """
    Returns today's name days
    Args:
        None

    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    url = "https://www.kalbi.pl/kalendarz-imienin"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        name_days = soup.find_all("p", itemprop="text")
        name_list = [name_day.text.replace("\xa0", " ") for name_day in name_days]
        return name_list[0]
    except Exception as e:
        raise e
