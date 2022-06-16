from aiogram import Bot
from aiogram.dispatcher import Dispatcher
# import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from base import config
storage = MemoryStorage()

bot = Bot(token=config.TG_API_KEY)
dp = Dispatcher(bot, storage=storage)