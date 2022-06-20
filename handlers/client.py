from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from base.init import bot, dp
from keyboards import kb_client
from dto.dto import FSMadd, FSMrunners
from logic import logic

# read1 = ()


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id, "Welcome to RunEvent bot",
            reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply(
            "Общение с ботом в ЛС, "
            "напишите ему:\nhttps://t.me/RunEventCS50x2022_bot"
        )


@dp.message_handler(commands=['add_runner'])
async def add_runner_command(message: types.Message):
    # await bot.send_message(message.from_user.id, 'we are add runner')
    await FSMadd.event_id.set()
    await message.reply("Enter event_id from Event list")


@dp.message_handler(state="*", commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


@dp.message_handler(state=FSMadd.event_id)
async def load_event_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = message.text
        data["name_runner"] = message.from_user.username

    await FSMadd.next()
    await message.reply("enter notes")


@dp.message_handler(state=FSMadd.run_notes)
async def load_notes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["notes"] = message.text

    async with state.proxy() as data:
        await logic.add_runner_command(state)

    await state.finish()


@dp.message_handler(commands=['delete_runner'])
async def delete_runner_command(message: types.Message):
    await bot.send_message(message.from_user.id, "we are delete runner")


@dp.message_handler(commands=['events_list'])
async def event_list_command(message: types.message):
    await logic.list_events(message)


@dp.message_handler(state=FSMrunners.peoples_id)
async def load_peoples_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data1:
        data1["id"] = message.text

    async with state.proxy() as data1:
        await logic.list_runners(state)

    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('show '))
async def callback_runner_list(cq: types.CallbackQuery):
    _, event_id, user_id = cq.data.split()
    runners = await logic.list_runners(event_id)
    await bot.send_message(
        user_id, str("\n".join(
            [f"Name of runner: {r[0]}, Note: {r[1]}"
             for r
             in runners])))


@dp.message_handler(commands='runners_list')
async def def_callback_run1(message: types.Message):
     events = await logic.list_events2()
     photo, name, date, distance, time, creator, id = 0, 1, 2, 3, 4, 5, 6
     for event in events:
        await bot.send_photo(
            message.from_user.id,
            event[photo],
            (f"{event[name]}\n"
             f"Date of Event: {event[date]}\n"
             f"Distance of run: {event[distance]}\n"
             f"Time of run: {event[time]}\n"
             f"Name of creator: {event[creator]}\n"
             f"Event ID: {event[id]}"))

        await bot.send_message(
            message.from_user.id,
            text='!!!!!!!',
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    f'Show list of runners for Event ID = {event[id]}',
                    callback_data=f'show {event[id]} {message.from_user.id}')))
