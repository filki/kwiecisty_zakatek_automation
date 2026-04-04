import asyncio
import logging
import os
import sys
import textwrap
from pathlib import Path

from dotenv import load_dotenv

# Ensure the package can be imported from src/
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.kwiaciarnia_monika.logger import setup_logger
from src.kwiaciarnia_monika.calendar_events import get_namedays_message
from src.kwiaciarnia_monika.telegram_bot import send_telegram_message

logger = logging.getLogger(__name__)


async def send_namedays_report(telegram_token: str, chat_id_token: str):
    """
    Sends today's name days report to Telegram.
    """
    try:
        name_days = get_namedays_message()
        logger.info(f"Name days fetched: {name_days}")

        message = textwrap.dedent(f"""
            Hej Monika, 
            dzisiaj imieniny obchodzą: {name_days}
            Miłego dnia! 🌸
        """).strip()

        await send_telegram_message(
            telegram_token=telegram_token,
            chat_id_token=chat_id_token,
            message_text=message,
        )
        logger.info("Name days report sent successfully")
    except Exception as e:
        logger.error(f"Error sending name days report: {e}")


async def main():
    """
    Main entry point for the morning report job.
    """
    load_dotenv()
    telegram_token = os.environ["TELEGRAM_TOKEN"]
    chatid_token = os.environ["TELEGRAM_CHAT_ID"]

    if not telegram_token or not chatid_token:
        logger.error("Missing Telegram tokens in environment variables")
        return

    await send_namedays_report(telegram_token, chatid_token)


if __name__ == "__main__":
    setup_logger()
    asyncio.run(main())
