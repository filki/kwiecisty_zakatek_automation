from loyverse_api import get_todays_receipts_data
import os
from dotenv import load_dotenv
import logging
from database import get_table_keys, add_receipts
"""
Syncs the database with the latest receipts from Loyverse
"""
load_dotenv()
DB_PATH = "/mnt/c/Users/ruder/Desktop/receipts.db"

def sync_db():
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
                add_receipts(data_corect, DB_PATH, key)
                logger.info(f"Data added to database")
        except Exception as e:
            logger.error(f"Error syncing database: {e}")

if __name__ == "__main__":
    sync_db()