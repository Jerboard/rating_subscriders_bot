from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.exceptions import TelegramForbiddenError

import logging
from datetime import datetime, timedelta
from apscheduler.triggers.interval import IntervalTrigger

import db
import keyboards as kb
from init import dp, bot, TZ, CHANNEL_ID, scheduler
from enums import UsersStatus


async def schedulers_start():
    scheduler.add_job(send_messages_sub, trigger=IntervalTrigger.interval, minutes=1)
    scheduler.start()


# проверяет подписку шлёт уведомления
async def send_messages_sub():
    users = await db.get_new_subscribers()
    ten_minutes_ago = datetime.now(TZ) - timedelta(minutes=10)
    for user in users:
        if TZ.localize(user.get_link_time) <= ten_minutes_ago:
            try:
                subscribe_info = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.user_id)
                if subscribe_info.status == ChatMemberStatus.LEFT:
                    referer = await db.get_user_info (user.referrer)
                    # await db.update_user (user_id=user.user_id, get_link_time=datetime.now (TZ))
                    text = 'Переходи в канал, не забудь подписаться'
                    await bot.send_message(
                        chat_id=user.user_id,
                        text=text,
                        reply_markup=kb.get_channel_link_kb (referer.invite_link))

                else:
                    await db.update_user (user_id=user.user_id, status=UsersStatus.SUBSCRIBER.value)
                    text = 'Теперь и ты можешь участвовать в акции, нажми Зарегистрироваться 👇👇'
                    await bot.send_message (
                        chat_id=user.user_id,
                        text=text,
                        reply_markup=kb.get_send_contact_kb())

            except TelegramForbiddenError as ex:
                await db.update_user (user_id=user.user_id, status=UsersStatus.BLOCKED_BOT.value)

            except Exception as ex:
                logging.warning(f'{datetime.now(TZ)}: {ex}')
