from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton


# def get_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
event_list = KeyboardButton("/events_list")
add_runner = KeyboardButton("/add_runner")
delete_runner = KeyboardButton("/delete_runner")
create_event = KeyboardButton("/create_event")
runner_list = KeyboardButton("/runners_list")
delete_event = KeyboardButton("/delete_event")

# add keys
keys = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keys.row(create_event).row(event_list, 
                           runner_list).row(add_runner, delete_runner)

# add admin keys
keysadmin = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keysadmin.row(create_event, delete_event).row(event_list, runner_list).row(
    add_runner, delete_runner
)
