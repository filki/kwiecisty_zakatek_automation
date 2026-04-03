import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.loyverse_api import get_todays_receipts_data,get_todays_customers_data
import os
from dotenv import load_dotenv
import logging
from core.database import get_table_keys, add_records_to_db
"""
Syncs the database with the latest receipts from Loyverse
"""
load_dotenv()
from config import DB_PATH

def sync_db_receipts():
    """
    Syncs the database with the latest receipts from Loyverse.

    Args:
        db_path (str): Path to the database.
        logger (logging.Logger): Logger.

    Returns:
        None

    Raises:
        sqlite3.Error: If the database operation fails.
    """
    logger = logging.getLogger(__name__)
    data = get_todays_receipts_data()
    logger.info(f"Data from Loyverse: {data}")
    if data is not None:
        try:
            data_list = [('receipt_headers', data[0]), ('receipt_items', data[1]), ('receipt_payments', data[2])]
            logger.info(f"Data list: {data_list}")
            for key, value in data_list:
                logger.info(f"Key: {key}")
                logger.info(f"Value: {value}")
                keys = get_table_keys(db_path=DB_PATH,table_name=key,unique_id='receipt_number')
                logger.info(f"Keys: {keys}")
                data_corect = value[~value["receipt_number"].isin(keys)]
                logger.info(f"Data corect: {data_corect}")
                add_records_to_db(data_corect, DB_PATH, key)
                logger.info(f"Data added to database")
        except Exception as e:
            logger.error(f"Error syncing database: {e}")
def sync_db_customers():
    """
    Syncs the database with the latest customers from Loyverse.

    Args:
        db_path (str): Path to the database.
        logger (logging.Logger): Logger.

    Returns:
        None

    Raises:
        sqlite3.Error: If the database operation fails.
    """
    logger = logging.getLogger(__name__)
    data = get_todays_customers_data()
    logger.info(f"Data from Loyverse: {data}")
    if data is not None:
        try:
            data_list = [('customers', data)]
            logger.info(f"Data list: {data_list}")
            for key, value in data_list:
                logger.info(f"Key: {key}")
                logger.info(f"Value: {value}")
                keys = get_table_keys(db_path=DB_PATH,table_name=key,unique_id='id')
                logger.info(f"Keys: {keys}")
                data_corect = value[~value["id"].isin(keys)]
                logger.info(f"Data corect: {data_corect}")
                add_records_to_db(data_corect, DB_PATH, key)
                logger.info(f"Data added to database")
        except Exception as e:
            logger.error(f"Error syncing database: {e}")
if __name__ == "__main__":
    sync_db_receipts()
    sync_db_customers()