from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from src.models.user import User
from sqlalchemy import update
from src.redis import redis

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, id: int):
    result = await db.execute(select(User).filter(User.id == id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_data):
    hashed_password = pwd_context.hash(user_data.password)
    db_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_users_list(db: AsyncSession, user_id: int):
    users = await db.execute(select(User).where(User.id != user_id))
    return users.scalars().all()


async def save_telegram_id(
        db: AsyncSession,
        user_id: int,
        telegram_id: int
):
    query = (
        update(User)
        .where(User.id == user_id)
        .values(telegram_id=telegram_id)
    )
    await db.execute(query)
    await db.commit()


async def is_user_online(user_id: int) -> bool:
    """Проверяет, находится ли пользователь в сети, по наличию токена в Redis."""
    return await redis.exists(f"auth_token:{user_id}") == 1
