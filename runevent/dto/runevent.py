from aiogram.dispatcher.filters.state import State, StatesGroup


# class for create event
class FSMAdmin(StatesGroup):
    photo = State()
    name_run = State()
    date_run = State()
    distance_run = State()
    time_run = State()
    name_creator = State()


# class for add runner
class FSMadd(StatesGroup):
    event_id = State()
    run_notes = State()


# class for delete runner from DB
class FSMdel(StatesGroup):
    ev_id = State()
    del_runner = State()
