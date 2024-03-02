from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType

from datetime import datetime, timedelta

import db
import keyboards as kb
from init import dp, TZ, bot, CHANNEL_ID, BOT_NAME, ADMINS
from utilits.message_util import send_invoice_link
from enums import ButtonText, UsersStatus, Callbacks

@dp.channel_post()
async def fff(msg: Message):
    print(msg.chat.id)


# первый экран
@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    if msg.from_user.id in ADMINS:
        await state.clear()
        await msg.answer(text='<b>Действия администратора:</b>', reply_markup=kb.get_main_admin_kb())
        return

    user_info = await db.get_user_info(msg.from_user.id)
    text_split = msg.text.split (' ')
    referrer_id = int (text_split [1]) if len (text_split) == 2 else None
    if not user_info:
        await db.add_user(
            user_id=msg.from_user.id,
            full_name=msg.from_user.full_name,
            username=msg.from_user.username,
            referrer=referrer_id
        )
        user_info = await db.get_user_info (msg.from_user.id)

    if user_info.status == UsersStatus.PARTICIPANT.value:
        await send_invoice_link(msg.from_user.id)

    elif referrer_id:
        referer = await db.get_user_info(referrer_id)
        await db.update_user(
            user_id=msg.from_user.id,
            status=UsersStatus.GET_LINK.value,
            get_link_time=datetime.now(TZ))
        text = (f'Привет! Присоединяйтесь к нам, {msg.from_user.full_name}!\n\n'
                f'Подпишитесь на канал, чтобы вовремя получить доступ к программе восстановления '
                f'организма для ВЗРОСЛЫХ и ДЕТЕЙ!👇')
        await msg.answer(text, reply_markup=kb.get_channel_link_kb(referer.invite_link))

    else:
        text = 'Для регистрации в акции нажми "Поделиться контактом" 👇👇'
        await msg.answer (text, reply_markup=kb.get_send_contact_kb ())


# второй экран
# @dp.message(lambda msg: msg.text == ButtonText.GET_LINK.value)
# async def command_start_handler(msg: Message, state: FSMContext) -> None:
#     text = 'Чтобы участвовать отправь свой контакт'
#     await msg.answer(text, reply_markup=kb.get_send_contact_kb())


# второй экран
@dp.message(lambda msg: msg.content_type == ContentType.CONTACT)
async def save_phone(msg: Message, state: FSMContext) -> None:
    invite_link = await bot.create_chat_invite_link(
        chat_id=CHANNEL_ID,
        name=msg.from_user.full_name[:32]
    )

    await db.update_user(
        user_id=msg.from_user.id,
        phone_number=msg.contact.phone_number,
        invite_link=invite_link.invite_link,
        status=UsersStatus.PARTICIPANT.value
    )
    await send_invoice_link (msg.from_user.id)


@dp.callback_query(lambda cb: cb.data.startswith(Callbacks.CLOSE.value))
async def admin_rating_start(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await state.clear()
