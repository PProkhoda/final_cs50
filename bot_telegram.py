from aiogram.utils import executor
from create_bot import dp



async def on_startup(_):
    print('bot online')
    
from handlers import client, admin

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)