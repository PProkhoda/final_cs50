from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from base import config

# add storage type
storage = MemoryStorage()

# create Bot and Dispatcher
bot = Bot(token=config.TG_API_KEY)
dp = Dispatcher(bot, storage=storage)
