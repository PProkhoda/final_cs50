from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types import CallbackQuery
from datetime import datetime
import aiogram.utils.markdown as md
from aiogram.types import ParseMode

from runevent.base.init import bot, dp, storage
from runevent.helpers.keyboard import keys
from runevent.dto.runevent import CreateEventFSM, AddRunnerFSM
from runevent.logic import runevent as logic


# ID = None
# chat_id = None


# hiden moderator handler, moderator = telegram administrator
# @dp.message_handler(commands="moderator", is_chat_admin=True)
# async def make_changes_command(message: Message):
#     # global ID
#     # ID = message.from_user.id
#     await bot.send_message(
#         message.from_user.id, "What happend?", reply_markup=keysadmin)
#     await message.delete()


# start handler
@dp.message_handler(commands=["start"])
async def command_start(message: Message):
    """start command

    Args:
        message (Message): start message
    """
    try:
        await bot.send_message(
            message.from_user.id, "Welcome to RunEvent bot", reply_markup=keys
        )
        await message.delete()
    except:
        await message.reply(
            "Communication with the bot in "
            "the PM, write to him:\nhttps://t.me/RunEventCS50x2022_bot"
        )


@dp.message_handler(commands=["help"])
async def command_help(message: Message):
    """
    help handler
    """
    try:
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


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: Message, state: FSMContext):
    """add cancel handler

    Args:
        message (Message): telegram message
        state (FSMContext): all state
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("OK")


@dp.message_handler(commands=["events_list"])
async def event_list_command(message: Message):
    """list of all events handler

    Args:
        message (Message): telegram message
    """
    chat_id = message.chat.id
    # breakpoint()
    events = await logic.list_events2(chat_id)
    name, date, distance, pace, creator, chat_id, time_start  = 1, 2, 3, 4, 5, 7, 8
    for event in events:
        if len(event) < 1:
            await bot.send_message(message.from_user.id,
                                   "list of runners is empty")
        else:
            await bot.send_message(
                message.from_user.id,
                text=(
                    f"Event name:{event[name]}\n"
                    f"Date of Event: {event[date]}\n"
                    f"Start time: {event[time_start]}\n"
                    f"Distance of run in km: {event[distance]}\n"
                    f"Running pace: {event[pace]}\n"
                    f"Name of creator: {event[creator]}\n"
                ),
            )
    await message.delete()


@dp.message_handler(commands="runners_list")
async def def_callback_run1(message: Message):
    """list of ruuners handler part1 (inline button)

    Args:
        message (Message): telegram message
    """
    chat_id = message.chat.id
    # breakpoint()
    events = await logic.list_events2(chat_id)
    name, date, distance, pace, id, chat_id, time_start  = 1, 2, 3, 4, 6, 7, 8
    for event in events:
        if len(event) < 1:
            await bot.send_message(message.from_user.id,
                                   "list of runners is empty")
        else:
            await bot.send_message(
                message.from_user.id,
                text=(
                    f"Event name:{event[name]}\n"
                    f"Date of Event: {event[date]}\n"
                    f"Start time: {event[time_start]}\n"
                    f"Distance of run in km: {event[distance]}\n"
                    f"Running pace: {event[pace]}\n"
                ),
            )

        await bot.send_message(
            message.from_user.id,
            text="***************",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    f"Show list of runners for Event name: {event[name]}",
                    callback_data=f"show {event[id]} {message.from_user.id} {event[name]}",
                )
            ),
        )
    await message.delete()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("show "))
async def callback_runner_list(cq: CallbackQuery):
    """list of runners handler part2 finish (inline button)

    Args:
        cq (CallbackQuery): find Callback data 
    """
    _, event_id, user_id, event_name = cq.data.split()
    runners = await logic.list_runners(event_id)
    if len(runners) < 1:
        await bot.send_message(
            user_id,
            f"For Event *{event_name}* - list of runners is empty"
            )
    else:
        await bot.send_message(
            user_id,
            str("\n".join([f"Name of runner: {r[0]}  "
                           " Note: {r[1]}" for r in runners])),
        )
    await cq.answer()


@dp.message_handler(commands='create_event')
async def cmd_create(message: Message, state: FSMContext):
    """
    Create event part 1 Conversation's entry point
    """
    # Set state
    await CreateEventFSM.name_run.set()
    # breakpoint()

    state.storage.data[str(state.user)] = state.storage.data[str(state.chat)]
    state.storage.data.pop(str(state.chat), None)
    state.chat = state.user
    async with state.proxy() as data:
        data["chat_id"] = message.chat.id
    await message.delete()
    await bot.send_message(message.from_user.id, "Hi there! Enter Event name!")


@dp.message_handler(state=CreateEventFSM.name_run)
async def load_name(message: Message, state: FSMContext):
    """add event part 2

    Args:
        message (Message): telegram message
        state (FSMContext): CreateeventFSM clas
    """
    async with state.proxy() as data:
        data["name_run"] = message.text
        
    await CreateEventFSM.next()
    await message.reply("enter event date, format YYYY-MM-DD")


@dp.message_handler(state=CreateEventFSM.date_run)
async def load_date(message: Message, state: FSMContext):
    """add event part 3

    Args:
        message (Message): telegram message
        state (FSMContext): CreateeventFSM class
    """
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
    await message.reply("Enter time of start")


@dp.message_handler(state=CreateEventFSM.start_time)
async def load_start_time(message: Message, state: FSMContext):
    """add event part 4

    Args:
        message (Message): telegram message
        state (FSMContext): CreateeventFSM class
    """
    async with state.proxy() as data:
        data["start_time"] = message.text
        if not logic.validate_time(data["start_time"]):
            await message.reply("Incorrect data format, should be HH:MM")
            return

    await CreateEventFSM.next()
    await message.reply("Enter distance in kilometers")


@dp.message_handler(lambda message: not message.text.isdigit(), state=CreateEventFSM.distance_run)
async def process_distance_invalid(message: Message):
    """add event part 4/1 Check distance. Distance gotta be digit

    Args:
        message (Message): telegram message

    Returns:
        message from bot: text
    """
    return await message.reply("Distance gotta be a number.\n"
                               "Enter distance in kilometers (digits only)")


@dp.message_handler(lambda message: message.text.isdigit(), state=CreateEventFSM.distance_run)
async def load_distance(message: Message, state: FSMContext):
    """add event handler part 5

    Args:
        message (Message): telegram message
        state (FSMContext): CreateeventFSM class
    """
    async with state.proxy() as data:
        data["distance_run"] = message.text

    await CreateEventFSM.next()
    await message.reply("enter Running pace")


@dp.message_handler(state=CreateEventFSM.time_run)
async def load_time(message: Message, state: FSMContext):
    """add event handler part 6 finish

    Args:
        message (Message): telegram message
        state (FSMContext): CreateEventFSM class
    """
    async with state.proxy() as data:
        data["time_run"] = message.text
        data["name_creator"] = message.from_user.username

    async with state.proxy() as data:
        await logic.add_event_command(state)
        m = await bot.send_message(
            data["chat_id"],
            md.text(
                md.text('Event name: ', md.bold(data["name_run"])),
                md.text('Event date:', data["date_run"]),
                md.text('Start time:', data["start_time"]),
                md.text('Distance of run in km:', data["distance_run"]),
                md.text('Running pace:', data["time_run"]),
                sep='\n',
            )
        )
        await m.pin()
    await message.reply("Event added")
    await state.finish()


# delete event handler part1 (only for moderator)
@dp.message_handler(commands="delete_event", is_chat_admin=True)
async def delete_event_start(message: Message):
    """delete event handler part1 (only for moderator)

    Args:
        message (Message): telegram message
    """
    chat_id = message.chat.id
    events = await logic.list_events2(chat_id)

    name, date, creator, id, chat_id = 1, 2, 5, 6, 7
    for event in events:
        await bot.send_message(
            message.from_user.id,
            text=(
                f"Event name:{event[name]}\n"
                f"Date of Event: {event[date]}\n"
                f"Name of creator: {event[creator]}\n"
            ),
        )

        await bot.send_message(
            message.from_user.id, text="***************",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f"Delete Event *{event[name]}*",
                                     callback_data=f"del {event[id]} {message.from_user.id} {event[name]}")
            ),
        )
    await message.delete()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("del "))
async def delete_event_finish(callback_query: CallbackQuery):
    """delete event hadler part2 finish (only for moderator)

    Args:
        callback_query (CallbackQuery): find callback data
    """
    _, event_id, user_id, event_name = callback_query.data.split()
    await logic.sql_delete_command(event_id)
    await callback_query.answer(
        text=f"Event *{event_name}* - deleted",
        show_alert=True)
    


@dp.message_handler(commands="delete_runner")
async def delete_runner(message: Message):
    """Delete runner handler part1 (inline button)

    Args:
        message (Message): telegram message
    """
    chat_id = message.chat.id
    events = await logic.list_events2(chat_id)
    name, date, id, chat_id = 1, 2, 6, 7
    for event in events:
        await bot.send_message(
            message.from_user.id,
            text=(
                f"Event name:{event[name]}\n"
                f"Date of Event: {event[date]}\n"
            ),
        )

        await bot.send_message(
            message.from_user.id,
            text="!!!!!!!",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    md.text('Delete runners for Event ', md.bold(event[name])),
                    callback_data=f"delete {event[id]} {message.from_user.id} {message.from_user.username}",
                )
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    await message.delete()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("delete "))
async def callback_delete_runner(cq: CallbackQuery):
    """Delete runner handler part2 finish (inline button)

    Args:
        cq (CallbackQuery): Callback data query
    """
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
    
    await cq.answer()


@dp.message_handler(commands="add_runner", state=None)
async def add_runner(message: Message):
    """Add of ruuners handler part1 (FSM + inline button)

    Args:
        message (Message): telegram message
    """
    await AddRunnerFSM.run_notes.set()
    await message.reply("enter notes")


@dp.message_handler(state=AddRunnerFSM.run_notes)
async def set_callback_add_runner(message: Message, state: FSMContext):
    """add of ruuners handler part2 finish (FSM + inline button)

    Args:
        message (Message): telegram message
        state (FSMContext): AddRunnerFSM
    """
    notes = message.text
    chat_id = message.chat.id
    events = await logic.list_events2(chat_id)

    name, date, creator, id, chat_id = 1, 2, 5, 6, 7
    for event in events:
        now = datetime.now()
        if date >= now:
            await bot.send_message(
                message.from_user.id,
                text=(
                    f"Event name:{event[name]}\n"
                    f"Date of Event: {event[date]}\n"
                    f"Name of creator: {event[creator]}\n"
                ),
            )

            await bot.send_message(
                message.from_user.id,
                text="*************",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        f"Write notes and push for Add runner where Event ID = {event[id]}",
                        callback_data=f"add {event[id]} {message.from_user.id} {message.from_user.username} {notes}",
                    )
                ),
            )

    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("add "))
async def callback_add_runner(cq: CallbackQuery):
    """Add runner handler part2 finish (inline button)

    Args:
        cq (CallbackQuery): Callback data finding
    """
    _, event_id, user_id, username, notes = cq.data.split()
    runner = (event_id, username, notes)
    await logic.add_runner_command(runner)
    await bot.send_message(user_id, "Runner added")
