from aiogram import Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram import Bot
from aiogram.enums import ParseMode

from dotenv import load_dotenv
from os import getenv
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from sqlalchemy.ext.asyncio import create_async_engine

import asyncio
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

load_dotenv ()
loop = asyncio.get_event_loop()
dp = Dispatcher()
bot = Bot(getenv("TOKEN"), parse_mode=ParseMode.HTML)

TZ = timezone('Europe/Moscow')

scheduler = AsyncIOScheduler(timezone=TZ)

DEBUG = bool(getenv('DEBUG'))

ENGINE = create_async_engine(url=getenv('DB_URL'))

DATE_FORMAT = getenv('DATE_FORMAT')
TIME_FORMAT = getenv('TIME_FORMAT')

CHANNEL_ID = int(getenv('CHANNEL_ID'))
BOT_NAME = getenv('BOT_NAME')

ADMINS = [524275902, 1456925942]


async def set_main_menu():
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Перезапустить'),
        BotCommand (command='/statistic',
                    description='Статистика')
    ]

    await bot.set_my_commands(main_menu_commands)