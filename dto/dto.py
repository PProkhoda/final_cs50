from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    photo = State()
    name_run = State()
    date_run = State()
    distance_run = State()
    time_run = State()
    name_creator = State()
    
class FSMadd(StatesGroup):
    event_id = State()
    run_notes = State()