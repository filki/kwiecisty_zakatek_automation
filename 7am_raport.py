"""
7am raport
"""
from asyncio.log import logger
from weather import get_weather
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio
from telegram_bot import send_telegram_message
import textwrap
load_dotenv()
telegram_token = os.getenv("TELEGRAM_TOKEN")
chatid_token = os.getenv("TELEGRAM_CHAT_ID")
logger.info("Getting weather data")

async def send_morning_weather_report():
    weather = get_weather()
    logger.info(f"Weather data: {weather}")


    await send_telegram_message(telegram_token=telegram_token,chat_id_token=chatid_token,message_text=
                                    textwrap.dedent(f"""
                                    Cześć Monika, obecna pogoda: {weather} stopni celsjusza.
                                    """)) 

asyncio.run(send_morning_weather_report())