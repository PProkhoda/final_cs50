from logic import logic
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

# from base import config
import config

storage = MemoryStorage()

bot = Bot(token=config.TG_API_KEY)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print("bot online")
    logic.sql_start()
