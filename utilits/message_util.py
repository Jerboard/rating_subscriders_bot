from aiogram.types import ReplyKeyboardRemove


from init import bot, BOT_NAME


async def send_invoice_link(user_id: int):
    referral_link = f'https://t.me/{BOT_NAME}?start={user_id}'
    text = (f'Это ваша реферальная ссылка. '
            f'Скопируйте ее и отправьте тому, кого хотите пригласить. Или разместите у себя в соц.сетях.'
            f'Засчитываются только те приглашенные, которые подписались на канал.\n'
            f'Чтобы узнать рейтинг и количество приглашенных нажмите кнопку Меню и Статистика.\n\n'
            f'Ваша ссылка👇👇👇\n'
            f'(нажми на нее и она скопируется)\n\n'
            f'<code>{referral_link}</code>')
    await bot.send_message(text, reply_markup=ReplyKeyboardRemove ())
