"""
Sends closing report to telegram.
"""
import asyncio
from database import get_rows_number,get_biggest_receipt_customer
import logging
from telegram_bot import send_telegram_message,send_telegram_document
from dotenv import load_dotenv
from datetime import datetime
import os
import textwrap
load_dotenv()
telegram_token = os.getenv("TELEGRAM_TOKEN")    
chatid_token = os.getenv("TELEGRAM_CHAT_ID")
from config import DB_PATH
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
    logging.basicConfig(level=logging.INFO,filename="main.log",format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    wynik = get_rows_number(db_path=DB_PATH,table_name='receipt_headers',unique_id='receipt_number')
    logger.info(f"Number of receipts: {wynik}")
    closing_report = f"""
        Cześć Monika, dzisiaj({now}) 
        do kasy wpłynęło {wynik} paragonów.
        Miłego wieczoru!
        """ 
    await send_telegram_message(telegram_token=telegram_token,chat_id_token=chatid_token,message_text=
                                    textwrap.dedent(closing_report))
    logger.info(f"Closing report sent to telegram")

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
        logger.info(f"Database copy sent to telegram")
    except Exception as e:
        logger.error(f"Error sending database copy: {e}")
async def send_customers_report():
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
    wynik = get_biggest_receipt_customer(db_path=DB_PATH,table_name='receipt_headers',unique_id='receipt_number')
    customers_report = f"""
        🌸 Cześć Monika, to był świetny dzień ({now})! 🌸
        Udało się zamknąć kasę! 
        Zestawienie twardych danych na dziś:
        🏆 Krezus Dnia: {wynik['name'].iloc[0]} 
        💸 Kwota zostawiona: {wynik['total_money'].iloc[0]} PLN
        Pamiętaj sprawdzić stany wody w wiadrach! Miłego wieczoru i odpoczywaj! 🌙

        """
    await send_telegram_message(telegram_token=telegram_token,chat_id_token=chatid_token,message_text=
                                    textwrap.dedent(customers_report))
    logger.info(f"Customers report sent to telegram")
    
asyncio.run(send_closing_report())
asyncio.run(send_database_copy())
asyncio.run(send_customers_report())