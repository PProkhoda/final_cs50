from aiogram import  types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text 

from create_bot import dp, bot
from keyboards import kb_client
from dto.dto import FSMadd
from logic import logic



# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Welcome to RunEvent bot', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом в ЛС, напишите ему:\nhttps://t.me/RunEventCS50x2022_bot')
        
# @dp.message_handler(commands=['add_runner'])
async def add_runner_command(message : types.Message):
    # await bot.send_message(message.from_user.id, 'we are add runner')
    await FSMadd.event_id.set()
    await message.reply('Enter event_id from Event list')
    
    
# @dp.message_handler(state="*", commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')
    

# @dp.message_handler(state=FSMadd.event_id)
async def load_event_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text  
        data['name_runner'] = message.from_user.username
        
    await FSMadd.next()
    await message.reply('enter notes')
    

    
# @dp.message_handler(state=FSMAdmin.run_notes)
async def load_notes(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['notes'] = message.text

    async with state.proxy() as data:
        await logic.add_runner_command(state)
    
    await state.finish()
    
# @dp.message_handler(commands=['delete_runner'])
async def delete_runner_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'we are delete runner')
    
# @dp.message_handler(commands=['events_list'])
# async def event_list_comand(message : types.message):
#     for ret in cur.execute('SELECT * FROM menu').fetchall():
#         await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
        
        
        
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(add_runner_command, commands=['add_runner'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(load_event_id, state=FSMadd.event_id)
    dp.register_message_handler(load_notes, state=FSMadd.run_notes)
    dp.register_message_handler(delete_runner_command, commands=['delete_runner'])
    # dp.register_message_handler(event_list_command, commands=['events_list'])
