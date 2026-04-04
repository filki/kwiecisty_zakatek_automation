"""
7am raport
"""

import sys
from pathlib import Path
from asyncio.log import logger

# from src.kwiaciarnia_monika.weather import get_weather
# from src.kwiaciarnia_monika.calendar_events import get_name_days
import os
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent))

load_dotenv()
telegram_token = os.getenv("TELEGRAM_TOKEN")
chatid_token = os.getenv("TELEGRAM_CHAT_ID")
logger.info("Getting weather data")


# async def send_morning_weather_report():
#     """
#     Sends morning weather report to telegram.

#     Args:
#         telegram_token (str): Telegram token.
#         chatid_token (str): Chat ID token.
#         logger (logging.Logger): Logger.

#     Returns:
#         None

#     Raises:
#         httpx.HTTPStatusError: If the HTTP request fails.
#     """
#     # weather = get_weather()
#     # logger.info(f"Weather data: {weather}")
#     name_days = get_name_days()
#     logger.info(f"Name days: {name_days}")
#     try:
#         await send_telegram_message(
#             telegram_token=telegram_token,
#             chat_id_token=chatid_token,
#             message_text=textwrap.dedent(f"""
#                                         Hej Monika,
#                                         {name_days}
#                                         Miłego dnia!
#                                         """),
#         )
#         logger.info(f"Weather report sent to telegram")
#     except Exception as e:
#         logger.error(f"Error sending weather report: {e}")


# if __name__ == "__main__":
#     asyncio.run(send_morning_weather_report())
