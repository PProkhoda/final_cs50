from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

# from aiogram.types import ReplyKeyboardRemove

b1 = KeyboardButton("/events_list")
b2 = KeyboardButton("/add_runner")
b3 = KeyboardButton("/delete_runner")
b4 = KeyboardButton("/create_event")
b5 = KeyboardButton("/runners_list")
b6 = KeyboardButton('/delete_event')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin.add(b4).insert(b6).add(b1).insert(b5).add(b2).insert(b3)