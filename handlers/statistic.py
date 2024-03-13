from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import db
import keyboards as kb
from init import dp, BOT_NAME, ADMINS
from enums import UsersStatus


# статистика пользователя
@dp.message(Command('statistic'))
async def get_user_statistic(msg: Message, state: FSMContext) -> None:
    if msg.from_user.id in ADMINS:
        await state.clear()
        await msg.answer(text='<b>Действия администратора:</b>', reply_markup=kb.get_main_admin_kb())
        return

    user_info = await db.get_user_info (msg.from_user.id)
    if user_info.status != UsersStatus.PARTICIPANT.value:
        text = ('Перейдите и подпишитесь на канал и вы тоже сможете получить персональную ссылку-приглашение '
                'для своих друзей, которым желаете ЗДОРОВЬЯ!')
        await msg.answer (text)

    else:
        my_referrers = await db.get_user_referrals(msg.from_user.id)
        all_referrers = 0
        subscribers = 0
        my_position = 0

        for user in my_referrers:
            all_referrers += 1
            if user.status == UsersStatus.SUBSCRIBER.value or user.status == UsersStatus.PARTICIPANT.value:
                subscribers += 1

        rating = await db.get_users_rating(limit=1000)

        find_position = False
        for user in rating:
            my_position += 1
            if user.referrer == msg.from_user.id:
                find_position = True
                break

        # Если никто не перешёл моя позиция последнее место +1
        if not find_position:
            my_position += 1

        referral_link = f'https://t.me/{BOT_NAME}?start={msg.from_user.id}'
        text = (f'Ваше место в рейтинге: {my_position}\n'
                f'Получили ссылку: {all_referrers}\n'
                f'Присоединились в канал: {subscribers}\n\n'
                f'<b>Напоминаю, ваша ссылка 👇</b>\n'
                f'(нажми на нее и она скопируется)\n'
                f'<code>{referral_link}</code>\n')
        await msg.answer(text)
