from aiogram.types import ReplyKeyboardRemove


from init import bot, BOT_NAME


async def send_invoice_link(user_id: int):
    referral_link = f'https://t.me/{BOT_NAME}?start={user_id}'
    text = (f'Это ваша ссылка-приглашение в канал Алёны Ковальчук «Сбрось Лишнее». Скопируйте её и отправьте '
            f'тому, кого хотите пригласить.\n'
            f'Также эту ссылку можно разместить у себя в социальных сетях.\n\n'
            f'Ваша ссылка👇👇👇\n'
            f'(нажмите на нее и она скопируется)\n\n'
            f'<code>{referral_link}</code>')
    await bot.send_message(chat_id=user_id, text=text, reply_markup=ReplyKeyboardRemove ())
