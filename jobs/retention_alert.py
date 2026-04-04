from config import DB_PATH
from dotenv import load_dotenv
import os
from typing import List
from pathlib import Path
import asyncio
from src.kwiaciarnia_monika.analytics import find_possible_churn
from src.kwiaciarnia_monika.telegram_bot import send_telegram_message
from src.kwiaciarnia_monika.logger import setup_logger
import textwrap

load_dotenv()


logger = setup_logger()
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]


async def send_retention_alert(churn_customers: List[dict], db_path: Path):
    for customer in churn_customers:
        customer_name = customer["customer_name"]
        message = f"""
        Cześć Monika, 
        Wygląda na to, że dawno nie było u nas {customer_name}.
        Może warto zadzwonić i zapytać co słychać?
        """
        await send_telegram_message(
            telegram_token=TELEGRAM_TOKEN,
            chat_id_token=TELEGRAM_CHAT_ID,
            message_text=textwrap.dedent(message),
        )
    logger.info(f"Sent retention alert to {len(churn_customers)} customers")


async def main():
    churn_customers = find_possible_churn(db_path=DB_PATH)
    await send_retention_alert(churn_customers=churn_customers, db_path=DB_PATH)


if __name__ == "__main__":
    asyncio.run(main())
