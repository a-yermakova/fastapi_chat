from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, WebSocket, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserCreate, UserOut, UserLogin
from src.services.auth import authenticate_user
from src.services.user import create_user, get_user_by_email, get_users_list
from src.db import get_async_session
from fastapi.security import OAuth2PasswordBearer
from src.utils.tokens import create_access_token, verify_access_token, store_token_in_redis, get_token_from_redis, \
    delete_token_from_redis

router = APIRouter(prefix="/users", tags=["Пользователи"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=UserOut)
async def register(
        user_data: Annotated[UserCreate, Body()],
        db: AsyncSession = Depends(get_async_session)
):
    db_user = await get_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(db, user_data)
    return new_user


@router.post("/login")
async def login(
        user_data: Annotated[UserLogin, Body()],
        db: AsyncSession = Depends(get_async_session)
):
    db_user = await authenticate_user(db, user_data.email, user_data.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"email": db_user.email, "id": db_user.id})
    await store_token_in_redis(user_id=str(db_user.id), token=access_token)
    return {"username": db_user.username, "access_token": access_token}


async def get_current_user_id_ws(websocket: WebSocket, user_token: str):
    try:
        payload = verify_access_token(user_token)
        user_id = payload.get("id")

        redis_token = await get_token_from_redis(str(user_id))

        if redis_token != user_token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        return user_id

    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None


async def get_current_user_id(
        token: str = Depends(oauth2_scheme),
):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    redis_token = await get_token_from_redis(str(user_id))

    if redis_token != token:
        raise HTTPException(
            status_code=401,
            detail="Token expired or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


@router.post("/logout")
async def logout(current_user_id: int = Depends(get_current_user_id)):
    await delete_token_from_redis(str(current_user_id))
    return {"msg": "Successfully logged out"}


@router.get("", response_model=List[UserOut])
async def get_all_users(
        db: AsyncSession = Depends(get_async_session),
        current_user_id: int = Depends(get_current_user_id)
):
    users = await get_users_list(db, current_user_id)
    return users
