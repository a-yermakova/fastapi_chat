from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.db import get_async_session
from src.services.auth import authenticate_user
from src.services.user import save_telegram_id

router = Router()


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я уведомлю тебя о новых сообщениях.\n"
                         "Для регистрации выполни команду /register")


class RegistrationState(StatesGroup):
    waiting_for_email = State()
    waiting_for_password = State()


@router.message(Command("register"))
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer("Введите ваш email:")
    await state.set_state(RegistrationState.waiting_for_email)


@router.message(RegistrationState.waiting_for_email, F.text)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Теперь введите ваш пароль:")
    await state.set_state(RegistrationState.waiting_for_password)


@router.message(RegistrationState.waiting_for_password, F.text)
async def process_password(
        message: types.Message,
        state: FSMContext,
):
    user_data = await state.get_data()
    email = user_data["email"]
    password = message.text
    async for db in get_async_session():
        user = await authenticate_user(db, email, password)
        if user:
            await save_telegram_id(db, user.id, message.from_user.id)
            await message.answer("Вы успешно зарегистрированы в системе!")
            await state.clear()
        else:
            await message.answer("Неверные email или пароль. Попробуйте еще раз.")
            await state.clear()


def register_handlers(dispatcher):
    dispatcher.include_router(router)
