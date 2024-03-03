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
    scheduler.add_job(send_messages_sub, trigger='interval', minutes=1)
    scheduler.start()


# проверяет подписку шлёт уведомления
async def send_messages_sub():
    users = await db.get_new_subscribers()
    ten_minutes_ago = datetime.now(TZ) - timedelta(minutes=5)
    one_hours_ago = datetime.now(TZ) - timedelta(hours=1)
    three_hours_ago = datetime.now(TZ) - timedelta(hours=3)
    for user in users:
        try:
            subscribe_info = None
            if TZ.localize(user.get_link_time) <= ten_minutes_ago and user.status == UsersStatus.GET_LINK.value:
                subscribe_info = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.user_id)

            elif TZ.localize(user.get_link_time) <= one_hours_ago and user.status == UsersStatus.GET_LINK_1.value:
                subscribe_info = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.user_id)

            elif TZ.localize (user.get_link_time) <= three_hours_ago and user.status == UsersStatus.GET_LINK_3.value:
                subscribe_info = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.user_id)

            if subscribe_info:
                subscribe_info = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.user_id)
                if subscribe_info.status == ChatMemberStatus.LEFT:
                    text = ('<b>Можно быть здоровым без БАДов и таблеток!</b>\n\n'
                            'Каждый рецепт и протокол в канале проходит экспертизу лучших врачей СНГ и состоит '
                            'только из натуральных ингредиентов. Такого нет НИ У КОГО!\n\n'
                            'Возможно вы перешли в канал, но не подписались.\n'
                            'Перейдите в канал, нажмите кнопку внизу в канале "Присоединиться или подписаться" и '
                            'закрепите себе канал, чтобы не пропустить анонс новой подборки уникальных протоколов '
                            'по восстановлению здоровья.\n\n'
                            '⌛️ И уже совсем скоро вы сможете получить персональную ссылку-приглашение для своих '
                            'друзей, которым желаете ЗДОРОВЬЯ!')
                    referer = await db.get_user_info (user.referrer)
                    await bot.send_message(
                        chat_id=user.user_id,
                        text=text,
                        reply_markup=kb.get_channel_link_kb (referer.invite_link))

                    if user.status == UsersStatus.GET_LINK.value:
                        await db.update_user (user_id=user.user_id, status=UsersStatus.GET_LINK_1.value)

                    elif user.status == UsersStatus.GET_LINK_1.value:
                        await db.update_user (user_id=user.user_id, status=UsersStatus.GET_LINK_3.value)

                    elif user.status == UsersStatus.GET_LINK_3.value:
                        await db.update_user (user_id=user.user_id, status=UsersStatus.NEW.value)

                else:
                    await db.update_user (user_id=user.user_id, status=UsersStatus.SUBSCRIBER.value)
                    text = (f'{user.full_name}, вы стали участником канала и теперь вы сможете получить '
                            f'персональную ссылку-приглашение для своих друзей, которым желаете ЗДОРОВЬЯ!\n\n'
                            f'Нажмите «Поделиться контактом», чтобы мы создали для вас ссылку.')
                    await bot.send_message (
                        chat_id=user.user_id,
                        text=text,
                        reply_markup=kb.get_send_contact_kb())

        except TelegramForbiddenError as ex:
            await db.update_user (user_id=user.user_id, status=UsersStatus.BLOCKED_BOT.value)

        except Exception as ex:
            logging.warning(f'{datetime.now(TZ)}: {ex}')
