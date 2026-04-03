"""
Loyverse API operations
"""

from loyverse import Client
from dotenv import load_dotenv
import os
import logging
from datetime import datetime,timezone,timedelta
import requests


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
        now = datetime.now(timezone.utc) - timedelta(days=1)
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