from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.message import Message


async def create_message(db: AsyncSession, message_data, sender_id: int):
    message = Message(
        sender_id=sender_id,
        recipient_id=message_data.recipient_id,
        content=message_data.content
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def get_message_list(db: AsyncSession, sender_id: int, recipient_id: int):
    messages = await db.execute(
        select(Message).filter(
            ((Message.sender_id == sender_id) & (Message.recipient_id == recipient_id)) |
            ((Message.sender_id == recipient_id) & (Message.recipient_id == sender_id))
    ).order_by(Message.timestamp)
    )

    return messages.scalars().all()
