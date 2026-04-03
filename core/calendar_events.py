"""
Calendar events operations
"""
import requests
from bs4 import BeautifulSoup
import datetime
def get_name_days():
    """
    Returns today's name days
    Args:
        None
    Returns:
        str: Today's name days
    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    url = "https://www.kalbi.pl/kalendarz-imienin"
    today = datetime.datetime.now().strftime("%d.%m.%Y")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e
    try:
        soup = BeautifulSoup(response.text, "html.parser")
        name_days = soup.find_all("p", itemprop="text")
        name_list = [name_day.text.replace('\xa0', ' ') for name_day in name_days]
        return name_list[0]
    except Exception as e:
        raise e
