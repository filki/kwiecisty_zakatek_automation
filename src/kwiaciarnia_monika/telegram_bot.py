"""
Telegram operations
"""

from pathlib import Path

import logging
from telegram import Bot


async def send_telegram_message(
    telegram_token: str, chat_id_token: str, message_text: str
):
    """
    Sends a message to a Telegram chat.

    Args:
        telegram_token (str): Telegram bot token.
        chat_id_token (str): Telegram chat ID.
        message_text (str): Message text.

    Returns:
        None

    Raise:
        telegram.error.TelegramError: If the message sending fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Sending telegram message")
    bot = Bot(token=telegram_token)
    logger.info("Successfully created telegram bot")
    await bot.send_message(chat_id=chat_id_token, text=message_text)
    logger.info("Successfully sent telegram message")


async def send_telegram_document(
    telegram_token: str, chat_id_token: str, file_path: Path
):
    """
    Sends a document to a Telegram chat.

    Args:
        telegram_token (str): Telegram bot token.
        chat_id_token (str): Telegram chat ID.
        file_path (str): Path to the file to send.

    Returns:
        None

    Raise:
        telegram.error.TelegramError: If the document sending fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Sending telegram document")
    bot = Bot(token=telegram_token)
    logger.info("Successfully created telegram bot")
    with open(file_path, "rb") as plik_bazy:
        await bot.send_document(
            chat_id=chat_id_token,
            document=plik_bazy,
            caption="Wykonano Kopię Zapasową!",
        )
    logger.info("Successfully sent telegram document")
