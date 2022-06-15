from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import  types, Dispatcher
from create_bot import dp

from dto.dto import FSMAdmin


# class FSMAdmin(StatesGroup):
#     photo = State()
#     name_run = State()
#     date_run = State()
#     distance_run = State()
#     time_run = State()
#     name_creator = State()


# new comment
    
    
# @dp.message_handler(commands='create_event', state=None)
async def cm_start(message : types.Message):
    await FSMAdmin.photo.set()
    await message.reply('Load label of run')


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    # async with state.proxy() as data:
    #     await message.reply(str(data))
    
    await FSMAdmin.name_run.set()
    await message.reply('enter event name')    
    
    
# @dp.message_handler(state=FSMAdmin.name_run)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_run'] = message.text
    # async with state.proxy() as data:
    #     await message.reply(str(data))
    
    await FSMAdmin.date_run.set()
    await message.reply('enter event date')


# @dp.message_handler(state=FSMAdmin.date_run)
async def load_date(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date_run'] = message.text
    # async with state.proxy() as data:
    #     await message.reply(str(data))
    
    await FSMAdmin.next()
    await message.reply('enter distance of event')


# @dp.message_handler(state=FSMAdmin.distance_run)
async def load_distance(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['distance_run'] = message.text
    # async with state.proxy() as data:
    #     await message.reply(str(data))
    
    await FSMAdmin.next()
    await message.reply('enter race duration')
    
    
# @dp.message_handler(state=FSMAdmin.time_run)
async def load_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time_run'] = message.text
    # async with state.proxy() as data:
    #     await message.reply(str(data))
    
    await FSMAdmin.next()
    await message.reply('enter creator name')
    
    
# @dp.message_handler(state=FSMAdmin.name_creator)
async def load_creator(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_creator'] = message.text
        
    async with state.proxy() as data:
        await message.reply(str(data))
    
    await state.finish()
    

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['create_event'], state=None)
    dp.register_message_handler(load_photo, content_types='photo', state=FSMAdmin.photo)
    dp.register_inline_handler(load_name, state=FSMAdmin.name_run)
    dp.register_inline_handler(load_date, state=FSMAdmin.date_run)
    dp.register_inline_handler(load_distance, state=FSMAdmin.distance_run)
    dp.register_inline_handler(load_time, state=FSMAdmin.time_run)
    dp.register_inline_handler(load_creator, state=FSMAdmin.name_creator)
    
