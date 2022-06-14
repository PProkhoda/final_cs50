from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardRemove

b1 = KeyboardButton('/events_list')
b2 = KeyboardButton('/add_runner')
b3 = KeyboardButton('/delete_runner')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).add(b2).insert(b3)