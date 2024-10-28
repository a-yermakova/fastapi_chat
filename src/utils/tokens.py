from jose import JWTError, jwt
from datetime import datetime, timedelta

from src.redis import redis
from config import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TOKEN_EXPIRE_SECONDS = 1800


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def store_token_in_redis(user_id: str, token: str):
    await redis.setex(f"auth_token:{user_id}", TOKEN_EXPIRE_SECONDS, token)


async def get_token_from_redis(user_id: str) -> str:
    return await redis.get(f"auth_token:{user_id}")


async def delete_token_from_redis(user_id: str):
    await redis.delete(f"auth_token:{user_id}")
