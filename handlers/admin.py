from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from base.init import bot, dp
from dto.dto import FSMAdmin
from logic import logic
from keyboards import kb_admin


ID = None


# hiden moderator handler, moderator = telegram administrator
@dp.message_handler(commands='moderator', is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(
        message.from_user.id, 'What happend?', reply_markup=kb_admin)
    await message.delete()


# create event handler part1
@dp.message_handler(commands='create_event', state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.photo.set()
    await message.reply("Load label of run")


# cancel handler
@dp.message_handler(state="*", commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


# add event part2
@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id

    await FSMAdmin.next()
    await message.reply("enter event name")


# add event part3
@dp.message_handler(state=FSMAdmin.name_run)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_run"] = message.text

    await FSMAdmin.next()
    await message.reply("enter event date")


# add event part 4
@dp.message_handler(state=FSMAdmin.date_run)
async def load_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["date_run"] = message.text

    await FSMAdmin.next()
    await message.reply("enter distance of event")


# add event handler part 5
@dp.message_handler(state=FSMAdmin.distance_run)
async def load_distance(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["distance_run"] = message.text

    await FSMAdmin.next()
    await message.reply("enter race duration")


# add event handler part6 finish
@dp.message_handler(state=FSMAdmin.time_run)
async def load_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["time_run"] = message.text
        data["name_creator"] = message.from_user.username

    async with state.proxy() as data:
        await logic.add_event_command(state)
    await message.reply("Event added")
    await state.finish()


# delete event hadler part2 finish
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await logic.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(
        text=f'{callback_query.data.replace("del ", "")} deleted',
        show_alert=True)


# delete event handler part1 (only for moderator)
@dp.message_handler(commands='delete')
async def def_callback_run(message: types.Message):
    if message.from_user.id == ID:
        read = await logic.list_events2()
        for x in read:
            await bot.send_photo(
                message.from_user.id,
                x[0],
                f"{x[1]}\nDate of Event: {x[2]}\nDistance "
                "of run: {x[3]}\n'Time of run: {x[4]}\n"
                "Name of creator: {x[5]}\n Event ID: {x[6]}",
            )
            await bot.send_message(
                message.from_user.id, text='!!!!!!!!',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Delete {x[6]}',
                callback_data=f'del {x[6]}')))
