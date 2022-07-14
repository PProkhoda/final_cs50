import asyncio
from aiogram.utils import executor
from runevent.base.init import dp
from runevent.logic.runevent import sql_start, go
from runevent.handlers import runevent as handlers


def main():
    """
    Initialize bot instance, storage and
    dispatcher and run the bot by starting
    poll for updates. Create SQL tables
    on startup.
    """
    # start function
    async def on_startup(_):
        print("bot online")
        sql_start()

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == "__main__":
    main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go())