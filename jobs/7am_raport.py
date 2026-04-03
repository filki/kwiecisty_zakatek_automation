"""
7am raport
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from asyncio.log import logger
from core.weather import get_weather
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio
from core.telegram_bot import send_telegram_message
import textwrap
load_dotenv()
telegram_token = os.getenv("TELEGRAM_TOKEN")
chatid_token = os.getenv("TELEGRAM_CHAT_ID")
logger.info("Getting weather data")

async def send_morning_weather_report():
    """
    Sends morning weather report to telegram.

    Args:
        telegram_token (str): Telegram token.
        chatid_token (str): Chat ID token.
        logger (logging.Logger): Logger.

    Returns:
        None

    Raises:
        httpx.HTTPStatusError: If the HTTP request fails.
    """
    weather = get_weather()
    logger.info(f"Weather data: {weather}")
    try:
        await send_telegram_message(telegram_token=telegram_token,chat_id_token=chatid_token,message_text=
                                        textwrap.dedent(f"""
                                        Cześć Monika, obecna pogoda: {weather} stopni celsjusza.
                                        """)) 
        logger.info(f"Weather report sent to telegram")
    except Exception as e:
        logger.error(f"Error sending weather report: {e}")

asyncio.run(send_morning_weather_report())