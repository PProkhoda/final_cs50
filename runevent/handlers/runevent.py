from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types import CallbackQuery
from datetime import datetime

from runevent.base.init import bot, dp
from runevent.helpers.keyboard import keys, keysadmin
from runevent.dto.runevent import CreateEventFSM, AddRunnerFSM
from runevent.logic import runevent as logic


# ID = None
# chat_id = None


# hiden moderator handler, moderator = telegram administrator
@dp.message_handler(commands="moderator", is_chat_admin=True)
async def make_changes_command(message: Message):
    # global ID
    # ID = message.from_user.id
    await bot.send_message(
        message.from_user.id, "What happend?", reply_markup=keysadmin)
    await message.delete()


# start handler
@dp.message_handler(commands=["start"])
async def command_start(message: Message):
    try:
        # global chat_id
        # chat_id = message.chat.id
        await bot.send_message(
            message.from_user.id, "Welcome to RunEvent bot", reply_markup=keys
        )
        await message.delete()
    except:
        await message.reply(
            "Communication with the bot in "
            "the PM, write to him:\nhttps://t.me/RunEventCS50x2022_bot"
        )


# help handler
@dp.message_handler(commands=["help"])
async def command_help(message: Message):
    try:
        # global chat_id
        # chat_id = message.chat.id
        await bot.send_message(
            message.from_user.id, """
            To work with the bot, use the commands from the group chat.\n
            event_list = ("/events_list")\n
            add_runner = ("/add_runner")\n
            delete_runner = ("/delete_runner")\n
            create_event = ("/create_event")\n
            runner_list = ("/runners_list")\n
            """
        )
        await message.delete()
    except:
        await message.reply(
            "Communication with the bot in "
            "the PM, write to him:\nhttps://t.me/RunEventCS50x2022_bot"
        )


# add cancel handler
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


# list of all events handler
@dp.message_handler(commands=["events_list"])
async def event_list_command(message: Message):
    chat_id = message.chat.id
    # breakpoint()
    events = await logic.list_events2(chat_id)
    photo, name, date, distance, time, creator, id = 0, 1, 2, 3, 4, 5, 6
    for event in events:
        if len(event) < 1:
            await bot.send_message(message.from_user.id,
                                   "list of runners is empty")
        else:
            await bot.send_photo(
                message.from_user.id,
                event[photo],
                (
                    f"{event[name]}\n"
                    f"Date of Event: {event[date]}\n"
                    f"Distance of run: {event[distance]}\n"
                    f"Time of run: {event[time]}\n"
                    f"Name of creator: {event[creator]}\n"
                    f"Event ID: {event[id]}"
                ),
            )


# list of runners handler part2 finish (inline button)
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("show "))
async def callback_runner_list(cq: CallbackQuery):
    _, event_id, user_id = cq.data.split()
    runners = await logic.list_runners(event_id)
    if len(runners) < 1:
        await bot.send_message(user_id, "list of runners is empty")
    else:
        await bot.send_message(
            user_id,
            str("\n".join([f"Name of runner: {r[0]}  "
                           " Note: {r[1]}" for r in runners])),
        )


# list of ruuners handler part1 (inline button)
@dp.message_handler(commands="runners_list")
async def def_callback_run1(message: Message):
    chat_id = message.chat.id
    # breakpoint()
    events = await logic.list_events2(chat_id)
    photo, name, date, distance, time, creator, id = 0, 1, 2, 3, 4, 5, 6
    for event in events:
        await bot.send_photo(
            message.from_user.id,
            event[photo],
            (
                f"{event[name]}\n"
                f"Date of Event: {event[date]}\n"
                f"Distance of run: {event[distance]}\n"
                f"Time of run: {event[time]}\n"
                f"Name of creator: {event[creator]}\n"
                f"Event ID: {event[id]}"
            ),
        )

        await bot.send_message(
            message.from_user.id,
            text="list of events up",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    f"Show list of runners for Event ID = {event[id]}",
                    callback_data=f"show {event[id]} {message.from_user.id}",
                )
            ),
        )
        await message.delete()


# create event handler part1
@dp.message_handler(commands="create_event")
async def cm_start(message: Message):
    # await CreateEventFSM.photo.set()
    # await message.reply("Load label of run")
    # breakpoint()

    chat_id = message.chat.id
    # async with state.proxy() as data:
    #     data["chat_id"] = chat_id
    # await bot.send_message(
    #     message.from_user.id, "Load label of run")
    # await message.delete()
    # await CreateEventFSM.next()
    await bot.send_message(
            message.from_user.id,
            text=f"Do you want to create event for chat ID = {chat_id}",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    "Load label of run",
                    callback_data=f"create {chat_id}",
                )
            ),
        )
    await message.delete()


# # create event part2 finish (inline button)
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("create "), state=None)
async def callback_create_event(cq: CallbackQuery, state: FSMContext):
    _, chat_id = cq.data.split()
    async with state.proxy() as data:
        data["chat_id"] = chat_id
    await CreateEventFSM.photo.set()
    


# add event part2
@dp.message_handler(content_types=["photo"], state=CreateEventFSM.photo)
async def load_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
        # chat_id = message.chat.id
        # data["chat_id"] = chat_id
    await CreateEventFSM.next()
    await message.reply("enter event name")


# add event part3
@dp.message_handler(state=CreateEventFSM.name_run)
async def load_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["name_run"] = message.text
        
    await CreateEventFSM.next()
    await message.reply("enter event date, format YYYY-MM-DD")


# add event part 4
@dp.message_handler(state=CreateEventFSM.date_run)
async def load_date(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["date_run"] = message.text
        if not logic.validate(data["date_run"]):
            await message.reply("Incorrect data format, should be YYYY-MM-DD")
            return
        now = datetime.now()
        if datetime.strptime(data["date_run"], '%Y-%m-%d') < now:
            await message.reply("Date must be greater than today")
            return

    await CreateEventFSM.next()
    await message.reply("enter distance of event")


# add event handler part 5
@dp.message_handler(state=CreateEventFSM.distance_run)
async def load_distance(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["distance_run"] = message.text

    await CreateEventFSM.next()
    await message.reply("enter race duration")


# add event handler part6 finish
@dp.message_handler(state=CreateEventFSM.time_run)
async def load_time(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["time_run"] = message.text
        data["name_creator"] = message.from_user.username

    async with state.proxy() as data:
        await logic.add_event_command(state)
    await message.reply("Event added")
    await state.finish()


# delete event hadler part2 finish (only for moderator)
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("del "))
async def delete_event_finish(callback_query: CallbackQuery):
    await logic.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(
        text=f"{callback_query.data.replace('del ', '')} deleted",
        show_alert=True)


# delete event handler part1 (only for moderator)
@dp.message_handler(commands="delete_event", is_chat_admin=True)
async def delete_event_start(message: Message):
    # if message.from_user.id == ID:
    chat_id = message.chat.id
    read = await logic.list_events2(chat_id)
    for x in read:
        await bot.send_photo(
            message.from_user.id,
            x[0],
            f"{x[1]}\nDate of Event: {x[2]}\nDistance "
            "of run: {x[3]}\n'Time of run: {x[4]}\n"
            "Name of creator: {x[5]}\n Event ID: {x[6]}",
        )
        await bot.send_message(
            message.from_user.id,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f"Delete {x[6]}",
                                     callback_data=f"del {x[6]}")
            ),
        )


# Delete runner handler part2 finish (inline button)
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("delete "))
async def callback_delete_runner(cq: CallbackQuery):
    _, event_id, user_id, username = cq.data.split()
    runners = await logic.list_runners(event_id)
    if len(runners) < 1:
        await bot.send_message(user_id, "list of runners is empty")
    else:
        for runner in runners:
            if str(runner[0]) == username:
                del_data = (event_id, username)
                await logic.del_runner_command(del_data)
                await bot.send_message(user_id, "Runner Deleted")
                return

        await bot.send_message(user_id, "You can only delete yourself")


# Delete runner handler part1 (inline button)
@dp.message_handler(commands="delete_runner")
async def delete_runner(message: Message):
    # echo_callback = 'delete'
    # text_callback = 'Delete runners for Event ID = '
    chat_id = message.chat.id
    events = await logic.list_events2(chat_id)
    photo, name, date, distance, time, creator, id = 0, 1, 2, 3, 4, 5, 6
    for event in events:
        await bot.send_photo(
            message.from_user.id,
            event[photo],
            (
                f"{event[name]}\n"
                f"Date of Event: {event[date]}\n"
                f"Distance of run: {event[distance]}\n"
                f"Time of run: {event[time]}\n"
                f"Name of creator: {event[creator]}\n"
                f"Event ID: {event[id]}"
            ),
        )

        await bot.send_message(
            message.from_user.id,
            text="!!!!!!!",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    f"Delete runners for Event ID = {event[id]}",
                    callback_data=f"delete {event[id]} {message.from_user.id} {message.from_user.username}",
                )
            ),
        )


# add of ruuners handler part1 (FSM + inline button)
@dp.message_handler(commands="add_runner", state=None)
async def add_runner(message: Message):
    await AddRunnerFSM.run_notes.set()
    await message.reply("enter notes")


# add of ruuners handler part2 finish (FSM + inline button)
@dp.message_handler(state=AddRunnerFSM.run_notes)
async def set_callback_add_runner(message: Message, state: FSMContext):
    # echo_callback = 'delete'
    # text_callback = 'Delete runners for Event ID = '
    notes = message.text
    chat_id = message.chat.id
    events = await logic.list_events2(chat_id)
    photo, name, date, distance, time, creator, id = 0, 1, 2, 3, 4, 5, 6
    for event in events:
        now = datetime.now()
        if date >= now:
            await bot.send_photo(
                message.from_user.id,
                event[photo],
                (
                    f"{event[name]}\n"
                    f"Date of Event: {event[date]}\n"
                    f"Distance of run: {event[distance]}\n"
                    f"Time of run: {event[time]}\n"
                    f"Name of creator: {event[creator]}\n"
                    f"Event ID: {event[id]}"
                ),
            )
            await bot.send_message(
                message.from_user.id,
                text="!!!!!!!",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        f"Write notes and push for Add runner where Event ID = {event[id]}",
                        callback_data=f"add {event[id]} {message.from_user.id} {message.from_user.username} {notes}",
                    )
                ),
            )

    await state.finish()


# Add runner handler part2 finish (inline button)
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("add "))
async def callback_add_runner(cq: CallbackQuery):
    _, event_id, user_id, username, notes = cq.data.split()
    runner = (event_id, username, notes)
    await logic.add_runner_command(runner)
    await bot.send_message(user_id, "Runner added")
