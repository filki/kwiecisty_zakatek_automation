"""
Loyverse API operations
"""

from loyverse import Client
from dotenv import load_dotenv
import os
import logging
from datetime import datetime,timezone,timedelta
import requests
import pandas as pd 

logger = logging.getLogger(__name__)

load_dotenv()
access_token = os.getenv('LOYVERSE_TOKEN')

def get_todays_receipts_data():
    """
    Downloads todays receipt data and converts it to a dataframe.
    
    Args:
        access_token (str): Access token for the Loyverse API.

    Returns:
        pd.DataFrame: DataFrame containing todays receipt data.

    Raise:
        requests.exceptions.RequestException: If the request to the Loyverse API fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Downloading todays receipts data")
    try:
        client = Client(access_token=access_token)
        now = datetime.now(timezone.utc)
        response = client.receipts.get_by_date(now)
        logger.info("Successfully downloaded todays receipts data")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading todays receipts data: {e}")
        return None

    if len(response['receipts']) == 0:
        logger.info("No receipts found for today")
        return None
    else:
        receipts_df = client.receipts.to_dataframes(response)
        logger.info("Successfully converted receipts data to dataframe")
    
    return receipts_df

def get_todays_customers_data():
    """
    Downloads todays customers data and converts it to a dataframe.
    
    Args:
        access_token (str): Access token for the Loyverse API.

    Returns:
        pd.DataFrame: DataFrame containing todays customers data.

    Raise:
        requests.exceptions.RequestException: If the request to the Loyverse API fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Downloading todays customers data")
    try:
        client = Client(access_token=access_token)
        now = datetime.now(timezone.utc)
        response = client.customers.get_by_query(limit = 250)
        logger.info("Successfully downloaded todays customers data")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading todays customers data: {e}")
        return None
    if len(response['customers']) == 0:
        logger.info("No customers found for today")
        return None
    else:
        customers_df = pd.DataFrame(response['customers'])
        logger.info("Successfully converted customers data to dataframe")
        return customers_df
def get_categories_data():
    """
    Downloads categories data and converts it to a dataframe.
    
    Args:
        access_token (str): Access token for the Loyverse API.

    Returns:
        pd.DataFrame: DataFrame containing categories data.

    Raise:
        requests.exceptions.RequestException: If the request to the Loyverse API fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Downloading categories data")
    try:
        client = Client(access_token=access_token)
        response = client.categories.get_all()
        logger.info("Successfully downloaded categories data")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading categories data: {e}")
        return None
    if len(response['categories']) == 0:
        logger.info("No categories found")
        return None
    else:
        categories_df = pd.DataFrame(response['categories'])
        logger.info("Successfully converted categories data to dataframe")
        return categories_df