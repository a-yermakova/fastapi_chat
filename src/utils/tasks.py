from celery import shared_task
from src.services.user import is_user_online
from src.telegram_bot.notifications import send_telegram_notification

from src.utils.websocket import manager


@shared_task
async def send_notification(params: dict):
    if await is_user_online(params['recipient_id']):
        await manager.send_message(params['recipient_id'], {
            "sender_id": params['sender_id'],
            "content": params['message_content'],
            "timestamp": str(params['message_timestamp'])
        })
    else:
        if params['recipient_telegram_id']:
            await send_telegram_notification(
                params['recipient_telegram_id'],
                f"У вас новое сообщение от пользователя {params['sender_username']}:\n"
                f"{params['message_content']}"
            )
