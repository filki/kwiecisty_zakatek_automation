"""
Sends closing report to telegram.
"""
import asyncio
from database import get_rows_number
import logging
from telegram_bot import send_telegram_message,send_telegram_document
from dotenv import load_dotenv
from datetime import datetime
import os
import textwrap
load_dotenv()
telegram_token = os.getenv("TELEGRAM_TOKEN")    
chatid_token = os.getenv("TELEGRAM_CHAT_ID")
DB_PATH = "/mnt/c/Users/ruder/Desktop/receipts.db"
now = datetime.now().strftime("%Y-%m-%d")
logger = logging.getLogger(__name__)
async def send_closing_report():
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
    await send_telegram_document(telegram_token, chatid_token, DB_PATH)
    logger.info(f"Database copy sent to telegram")

asyncio.run(send_closing_report())
asyncio.run(send_database_copy())