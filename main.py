import asyncio
import logging
import sys

from handlers import dp
from init import set_main_menu, bot, DEBUG
from db.base import init_models
from utilits.check_subscribe import schedulers_start


async def main() -> None:
    await init_models()
    await schedulers_start()
    await set_main_menu()
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DEBUG:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        logging.basicConfig (level=logging.WARNING, filename='log.log')
    asyncio.run(main())
