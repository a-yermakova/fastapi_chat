from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.user import get_current_user_id, get_current_user_id_ws
from src.schemas.message import MessageCreate, MessageOut
from src.db import get_async_session

from src.services.message import create_message, get_message_list
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Annotated
from src.redis import redis
from src.services.user import get_user_by_id
from src.utils.tasks import send_notification
from src.utils.tokens import TOKEN_EXPIRE_SECONDS
from src.utils.websocket import manager

router = APIRouter(prefix="/messages", tags=["Сообщения"])


@router.post("/send", response_model=MessageOut)
async def send_message(
        message_data: Annotated[MessageCreate, Body()],
        db: AsyncSession = Depends(get_async_session),
        current_user_id: int = Depends(get_current_user_id)
):
    recipient = await get_user_by_id(db, message_data.recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    token_key = f"auth_token:{current_user_id}"
    if await redis.exists(token_key):
        await redis.expire(token_key, TOKEN_EXPIRE_SECONDS)

    new_message = await create_message(db, message_data, sender_id=current_user_id)
    sender = await get_user_by_id(db, current_user_id)
    notification_params = {
        'sender_id': sender.id,
        'sender_username': sender.username,
        'recipient_id': recipient.id,
        'recipient_telegram_id': recipient.telegram_id,
        'message_content': new_message.content,
        'message_timestamp': new_message.timestamp
    }
    await send_notification.run(notification_params)

    return new_message


@router.get("/history/{recipient_id}", response_model=List[MessageOut])
async def get_message_history(
        recipient_id: int,
        db: AsyncSession = Depends(get_async_session),
        current_user_id: int = Depends(get_current_user_id)
):
    messages = await get_message_list(db, current_user_id, recipient_id)

    return messages


@router.websocket("/ws/{user_token}")
async def websocket_endpoint(websocket: WebSocket, user_token: str):
    current_user_id: int = await get_current_user_id_ws(websocket, user_token)

    if current_user_id is None:
        return

    await manager.connect(current_user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(current_user_id, websocket)
