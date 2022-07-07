from aiogram.dispatcher.filters.state import State, StatesGroup


# class for create event
class CreateEventFSM(StatesGroup):
    # chat_id = State()
    # photo = State()
    name_run = State()
    date_run = State()
    start_time = State()
    distance_run = State()
    time_run = State()
    name_creator = State()


# class for add runner
class AddRunnerFSM(StatesGroup):
    # event_id = State()
    run_notes = State()


# class for delete runner from DB
class DelRunnerFSM(StatesGroup):
    ev_id = State()
    del_runner = State()
