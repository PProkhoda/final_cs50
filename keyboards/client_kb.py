from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardRemove

b1 = KeyboardButton('/events_list')
b2 = KeyboardButton('/add_runner')
b3 = KeyboardButton('/delete_runner')
b4 = KeyboardButton('/create_event')
b5 = KeyboardButton('/runner_list')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b4).add(b1).insert(b5).insert(b2).insert(b3)