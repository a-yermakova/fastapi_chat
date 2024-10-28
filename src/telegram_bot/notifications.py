from src.telegram_bot.bot import bot
import logging


async def send_telegram_notification(telegram_id: int, message_text: str):
    try:
        await bot.send_message(chat_id=telegram_id, text=message_text)
    except Exception as e:
        logging.error(f"Ошибка при отправке уведомления: {e}")
