from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from base.init import bot, dp
from keyboards import kb_client
from dto.dto import FSMadd, FSMdel
from logic import logic


# start/help handler
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(
            message.from_user.id, "Welcome to RunEvent bot",
            reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply(
            "Communication with the bot in "
            "the PM, write to him:\nhttps://t.me/RunEventCS50x2022_bot"
        )


# add runner handler part1
@dp.message_handler(commands=['add_runner'])
async def add_runner_command(message: types.Message):
    await FSMadd.event_id.set()
    await message.reply("Enter event_id from Event list")


# add cancel handler
@dp.message_handler(state="*", commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


# add runner handler part2
@dp.message_handler(state=FSMadd.event_id)
async def load_event_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = message.text
        data["name_runner"] = message.from_user.username

    await FSMadd.next()
    await message.reply("enter notes")


# add runner Handler part3 (finish)
@dp.message_handler(state=FSMadd.run_notes)
async def load_notes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["notes"] = message.text

    async with state.proxy() as data:
        await logic.add_runner_command(state)
    await message.reply("Runner added")
    await state.finish()


# list of all events handler
@dp.message_handler(commands=['events_list'])
async def event_list_command(message: types.message):
    await logic.list_events(message)


# list of runners handler part2 finish (inline button)
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('show '))
async def callback_runner_list(cq: types.CallbackQuery):
    _, event_id, user_id = cq.data.split()
    runners = await logic.list_runners(event_id)
    if len(runners) < 1:
        await bot.send_message(user_id, "list of runners is empty")
    else:
        await bot.send_message(
            user_id, str("\n".join(
                [f"Name of runner: {r[0]}, Note: {r[1]}"
                    for r in runners])))


# list of ruuners handler part1 (inline button)
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


# delete runner handler part1
@dp.message_handler(commands=['delete_runner'])
async def add_del_runner_command(message: types.Message):
    await FSMdel.ev_id.set()
    await message.reply("Enter event_id from Event list")


# delete runner handler part2
@dp.message_handler(state=FSMdel.ev_id)
async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = message.text
        runners = await logic.list_runners(data['id'])
        username = message.from_user.username
        for runner in runners:
            if str(runner[0]) == username:
                await message.reply(
                    "You in list. Do you want to delete yourself?   (y|n)")
                return await FSMdel.next()

        await bot.send_message(message.from_user.id,
                               "You can only delete yourself")
        await state.finish()


# delete runner handler part3 finish
@dp.message_handler(state=FSMdel.del_runner)
async def delete_runner(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['key'] = message.text
        username = message.from_user.username
        # await bot.send_message(message.from_user.id, data['id'])
        if str(data['key']) == str('y'):
            del_data = (data['id'], username)
            await logic.del_runner_command(del_data)
            await bot.send_message(message.from_user.id, "Runner Deleted")
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Delete canceled")
            await state.finish()
