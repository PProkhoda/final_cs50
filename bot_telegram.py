from aiogram.utils import executor

from create_bot import dp
from logic import logic
from handlers import client, admin


async def on_startup(_):
    print("bot online")
    logic.sql_start()


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
