from aiogram import  types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Welcome to RunEvent bot', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом в ЛС, напишите ему:\nhttps://t.me/RunEventCS50x2022_bot')
        
# @dp.message_handler(commands=['add runner'])
async def add_runner_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'we are add runner')
    
# @dp.message_handler(commands=['delete runner'])
async def delete_runner_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'we are delete runner')
    
# @dp.message_handler(commands=['events list'])
# async def event_list_comand(message : types.message):
#     for ret in cur.execute('SELECT * FROM menu').fetchall():
#         await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
        
        
        
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(add_runner_command, commands=['add runner'])
    dp.register_message_handler(delete_runner_command, commands=['delete runner'])
    # dp.register_message_handler(event_list_command, commands=['events list'])