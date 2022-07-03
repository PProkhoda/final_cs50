import sqlite3 as sq
from datetime import datetime
from runevent.base.init import bot


# from base.init import bot
db = None
cur = None


# create ore connect to DB
def sql_start():
    global db, cur
    db = sq.connect("event.db")
    cur = db.cursor()
    if db:
        print("Data base conected")
    db.execute("""
               CREATE TABLE IF NOT EXISTS events_list
                (photo TEXT, name_run TEXT, date_run TEXT,
                distance_run TEXT, time_run TEXT, name_creator
                TEXT, event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                chat_id INTEGER NOT NULL)
               """)
    db.execute("""
               CREATE TABLE IF NOT EXISTS peoples_list
               (id TEXT, name_runner TEXT NOT NULL,
               notes TEXT, FOREIGN KEY(id) REFERENCES events_list(event_id))
               """)

    db.commit()


# validate input date
def validate(date_text):
    try:
        return bool(datetime.strptime(date_text, '%Y-%m-%d'))
    except ValueError:
        return False


# add event to DB
async def add_event_command(state):
    async with state.proxy() as data:
        cur.execute("""
            INSERT INTO events_list(
            photo, name_run, date_run, distance_run,
             time_run, name_creator, chat_id)
             VALUES (?, ?, ?, ?, ?, ?, ?)
            """, tuple(data.values()))
        db.commit()


# add runner to DB
async def add_runner_command(state):
    cur.execute("INSERT INTO peoples_list VALUES(?, ?, ?)", tuple(state))
    db.commit()


# view list of all events from DB
# async def list_events(message):
#     for x in cur.execute("SELECT * FROM events_list").fetchall():
#         if len(x) < 1:
#             await bot.send_message(message.from_user.id,
#                                    "list of runners is empty")
#         else:
#             await bot.send_photo(
#                 message.from_user.id,
#                 x[0],
#                 f"{x[1]}\n"
#                 f"Date of Event: {x[2]}\n"
#                 f"Distance of run: {x[3]}\n"
#                 f"Time of run: {x[4]}\n"
#                 f"Name of creator: {x[5]}\n"
#                 f"Event ID: {x[6]}\n"
#                 f"chat ID: {x[7]}",
#             )


# select list of runners from DB
async def list_runners(data):
    return cur.execute(
        (
            """
            SELECT
             peoples_list.name_runner,
             peoples_list.notes
             FROM peoples_list
             INNER JOIN events_list
             ON peoples_list.id=events_list.event_id
             WHERE event_id == ?
            """
        ),
        (data,),
    ).fetchall()


# tuple evets from db
async def list_events2(chat_id):
    # breakpoint()
    return cur.execute("SELECT * FROM events_list WHERE chat_id == ?",
                       (chat_id, )).fetchall()


# delete event in DB
async def sql_delete_command(data):
    cur.execute("DELETE FROM events_list WHERE event_id == ?", (data,))
    db.commit()


# select all rows from peoples_list
async def list_runners2(data):
    cur.execute("SELECT * FROM peoples_list WHERE id == ?",
                tuple(data.values()))


# delete runner from DB via event_id
async def del_runner_command(data):
    # async with state.proxy() as data:
    cur.execute(
        "DELETE FROM peoples_list WHERE id == ? AND name_runner == ?",
        tuple(data)
    )
    db.commit()
