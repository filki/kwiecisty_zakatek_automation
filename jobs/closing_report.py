import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.kwiaciarnia_monika.logger import setup_logger
import asyncio
from src.kwiaciarnia_monika.database import (
    get_rows_number,
    get_biggest_receipt_customer,
)
import logging
from src.kwiaciarnia_monika.telegram_bot import (
    send_telegram_message,
    send_telegram_document,
)
from dotenv import load_dotenv
from datetime import datetime
import os
import textwrap
from config import DB_PATH

load_dotenv()
telegram_token = os.environ["TELEGRAM_TOKEN"]
chatid_token = os.environ["TELEGRAM_CHAT_ID"]


now = datetime.now().strftime("%Y-%m-%d")
logger = logging.getLogger(__name__)


async def send_closing_report():
    """
    Sends closing report to telegram.

    Args:
        telegram_token (str): Telegram token.
        chatid_token (str): Chat ID token.
        db_path (str): Path to the database.
        now (str): Current date.
        logger (logging.Logger): Logger.

    Returns:
        None

    Raises:
        sqlite3.Error: If the database operation fails.
    """

    wynik = get_rows_number(
        db_path=DB_PATH, table_name="receipt_headers", unique_id="receipt_number"
    )
    logger.info(f"Number of receipts: {wynik}")
    closing_report = f"""
        Cześć Monika, dzisiaj({now}) 
        do kasy wpłynęło {wynik} paragonów.
        Miłego wieczoru!
        """
    await send_telegram_message(
        telegram_token=telegram_token,
        chat_id_token=chatid_token,
        message_text=textwrap.dedent(closing_report),
    )
    logger.info("Closing report sent to telegram")


async def send_database_copy():
    """
    Sends database copy to telegram.

    Args:
        telegram_token (str): Telegram token.
        chatid_token (str): Chat ID token.
        db_path (str): Path to the database.
        logger (logging.Logger): Logger.

    Returns:
        None

    Raises:
        sqlite3.Error: If the database operation fails.
    """
    try:
        await send_telegram_document(telegram_token, chatid_token, DB_PATH)
        logger.info("Database copy sent to telegram")
    except Exception as e:
        logger.error(f"Error sending database copy: {e}")


async def send_biggest_receipt_customer():
    """
    Sends customers report to telegram.

    Args:
        telegram_token (str): Telegram token.
        chatid_token (str): Chat ID token.
        db_path (str): Path to the database.
        now (str): Current date.
        logger (logging.Logger): Logger.

    Returns:
        None

    Raises:
        sqlite3.Error: If the database operation fails.
    """
    wynik = get_biggest_receipt_customer(db_path=DB_PATH)
    customers_report = f"""
        🌸 Cześć Monika, to był świetny dzień ({now})! 🌸
        Udało się zamknąć kasę! 
        Zestawienie twardych danych na dziś:
        🏆 Krezus Dnia: {wynik["name"]} 
        💸 Kwota zostawiona: {wynik["total_money"]} PLN
        Pamiętaj sprawdzić stany wody w wiadrach! Miłego wieczoru i odpoczywaj! 🌙

        """
    await send_telegram_message(
        telegram_token=telegram_token,
        chat_id_token=chatid_token,
        message_text=textwrap.dedent(customers_report),
    )
    logger.info("Customers report sent to telegram")


async def main():
    setup_logger()
    await send_closing_report()
    await send_database_copy()
    await send_biggest_receipt_customer()


if __name__ == "__main__":
    asyncio.run(main())
