import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from src.telegram_bot.handlers import register_handlers
from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN, session=AiohttpSession())
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


async def set_commands():
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Начать взаимодействие"),
            BotCommand(command="register", description="Регистрация Telegram ID"),
        ]
    )


def register_all_handlers(dispatcher: Dispatcher):
    register_handlers(dispatcher)


async def start_bot():
    await set_commands()
    register_all_handlers(dp)
    await dp.start_polling(bot)
    