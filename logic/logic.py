import sqlite3 as sq
from create_bot import bot


def sql_start():
    global db, cur
    db = sq.connect("event.db")
    cur = db.cursor()
    if db:
        print("Data base conected")
    db.execute(
        "CREATE TABLE IF NOT EXISTS events_list (photo TEXT, name_run TEXT, date_run TEXT, distance_run TEXT, time_run TEXT, name_creator TEXT, event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL)"
    )
    db.execute(
        "CREATE TABLE IF NOT EXISTS peoples_list (id TEXT, name_runner TEXT NOT NULL, notes TEXT, FOREIGN KEY(id) REFERENCES events_list(event_id))"
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
        cur.execute("INSERT INTO peoples_list VALUES(?, ?, ?)", tuple(data.values()))
        db.commit()


async def list_events(message):
    for x in cur.execute("SELECT * FROM events_list").fetchall():
        await bot.send_photo(
            message.from_user.id,
            x[0],
            f"{x[1]}\nDate of Event: {x[2]}\nDistance of run: {x[3]}\n'Time of run: {x[4]}\nName of creator: {x[5]}\n Event ID: {x[6]}",
        )


async def list_runners(state):
    async with state.proxy() as data1:
        # await message.reply(str(data1))
        for y in cur.execute(
            'SELECT peoples_list.name_runner, peoples_list.notes FROM peoples_list INNER JOIN events_list ON peoples_list.id=events_list.event_id WHERE event_id= "?"',
            data1["id"],
        ).fetchall():
            await bot.send_message(y)
