import sqlite3 as sq
from base.init import bot
# from base.init import bot


def sql_start():
    global db, cur
    db = sq.connect('event.db')
    cur = db.cursor()
    if db:
        print("Data base conected")
    db.execute(
        "CREATE TABLE IF NOT EXISTS events_list ("
        "photo TEXT, name_run TEXT, date_run TEXT, "
        "distance_run TEXT, time_run TEXT, "
        "name_creator TEXT, "
        "event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)"
        )
    db.execute(
        "CREATE TABLE IF NOT EXISTS peoples_list (id TEXT, "
        "name_runner TEXT NOT NULL, "
        "notes TEXT, "
        "FOREIGN KEY(id) REFERENCES events_list(event_id))"
    )
    db.commit()


async def add_event_command(state):
    async with state.proxy() as data:
        cur.execute(
            "INSERT INTO events_list("
            "photo, name_run, date_run, distance_run, time_run, name_creator) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            tuple(data.values()),
        )
        db.commit()


async def add_runner_command(state):
    async with state.proxy() as data:
        cur.execute(
            "INSERT INTO peoples_list VALUES(?, ?, ?)", tuple(data.values()))
        db.commit()


async def list_events(message):
    for x in cur.execute("SELECT * FROM events_list").fetchall():
        await bot.send_photo(
            message.from_user.id,
            x[0],
            f'{x[1]}\n'
            f'Date of Event: {x[2]}\n'
            f'Distance of run: {x[3]}\n'
            f'Time of run: {x[4]}\n'
            f'Name of creator: {x[5]}\n'
            f'Event ID: {x[6]}',
        )


async def list_runners(data):
    return cur.execute(
        (
            'SELECT '
            'peoples_list.name_runner,'
            'peoples_list.notes '
            'FROM peoples_list '
            'INNER JOIN events_list'
            ' ON peoples_list.id=events_list.event_id '
            'WHERE event_id == ?'), (data,)).fetchall()


async def list_events2():
    return cur.execute("SELECT * FROM events_list").fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE '
                'FROM events_list WHERE event_id == ?', (data,))
    db.commit()


async def list_runners2(data):
    cur.execute(
        'SELECT * FROM peoples_list WHERE id == ?', tuple(data.values()))


async def del_runner_command(data):
    # async with state.proxy() as data:
    cur.execute(
        'DELETE FROM peoples_list WHERE id == ? AND name_runner == ?',
        tuple(data))
    db.commit()
