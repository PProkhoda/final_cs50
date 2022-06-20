from aiogram.utils import executor
from base.init import dp
from logic import logic
import handlers


# start function
async def on_startup(_):
    print("bot online")
    logic.sql_start()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
