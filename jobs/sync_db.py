import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.kwiaciarnia_monika.logger import setup_logger
from src.kwiaciarnia_monika.loyverse_api import (
    get_todays_receipts_data,
    get_todays_customers_data,
)
from dotenv import load_dotenv
from src.kwiaciarnia_monika.database import get_table_keys, add_records_to_db
from config import DB_PATH
import logging
import asyncio
import pandas as pd

logger = logging.getLogger(__name__)


load_dotenv()


async def save_today_receipts():
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
    data = get_todays_receipts_data()
    logger.info(f"Data from Loyverse: {data}")
    if data is not None:
        try:
            data_list = [
                ("receipt_headers", data[0]),
                ("receipt_items", data[1]),
                ("receipt_payments", data[2]),
            ]
            logger.info(f"Data list: {data_list}")
            for key, value in data_list:
                logger.info(f"Key: {key}")
                logger.info(f"Value: {value}")
                keys = get_table_keys(
                    db_path=DB_PATH, table_name=key, unique_id="receipt_number"
                )
                logger.info(f"Keys: {keys}")
                data_correct = value[~value["receipt_number"].isin(keys)]
                assert isinstance(data_correct, pd.DataFrame)
                add_records_to_db(data_correct, DB_PATH, key)
                logger.info("Data added to database")
        except Exception as e:
            logger.error(f"Error syncing database: {e}")


async def sync_db_customers():
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
    data = get_todays_customers_data()
    logger.info(f"Data from Loyverse: {data}")
    if data is not None:
        try:
            data_list = [("customers", data)]
            logger.info(f"Data list: {data_list}")
            for key, value in data_list:
                logger.info(f"Key: {key}")
                logger.info(f"Value: {value}")
                keys = get_table_keys(db_path=DB_PATH, table_name=key, unique_id="id")
                logger.info(f"Keys: {keys}")
                data_correct = value[~value["id"].isin(keys)]
                assert isinstance(data_correct, pd.DataFrame)
                add_records_to_db(data_correct, DB_PATH, key)
                logger.info("Data added to database")
        except Exception as e:
            logger.error(f"Error syncing database: {e}")


async def main():
    setup_logger()
    await save_today_receipts()
    await sync_db_customers()


if __name__ == "__main__":
    asyncio.run(main())
