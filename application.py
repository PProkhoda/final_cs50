from aiogram.utils import executor
from runevent.base.init import dp
from runevent.logic import runevent
import runevent.handlers


# start function
async def on_startup(_):
    print("bot online")
    runevent.sql_start()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
