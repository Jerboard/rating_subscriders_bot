from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums.content_type import ContentType

from asyncio import sleep
from datetime import datetime, timedelta

import db
import keyboards as kb
from init import dp, TZ, bot, CHANNEL_ID, BOT_NAME, ADMINS
from enums import ButtonText, UsersStatus, Callbacks


@dp.callback_query(lambda cb: cb.data.startswith(Callbacks.ADMIN_STATISTIC.value))
async def admin_statistic(cb: CallbackQuery):
    # ссылку получили (пришёл по ссылке и подписался)
    # всего перешло (пришёл по ссылке и подписался)

    participants = await db.get_all_participant()
    subscribers = await db.get_all_subscriber()

    text = (f'<b>Приглашающие:</b> {len(participants)}\n'
            f'<b>Приглашённые:</b> {len(subscribers)}\n\n')

    users_rating = await db.get_users_rating()
    text = f'{text}<b>Лучшие участники:</b>\n\n'
    for row in users_rating:
        user_info = await db.get_user_info(row.referrer)
        if user_info:
            text = f'{text}{user_info.full_name} - {row.points} подписчиков\n'

    if len(text) > 2000:
        text = f'{text[:2000]}...'

    await cb.message.answer(text)


@dp.callback_query(lambda cb: cb.data.startswith(Callbacks.ADMIN_RATING_START.value))
async def admin_rating_start(cb: CallbackQuery, state: FSMContext):
    await state.set_state(Callbacks.ADMIN_RATING_START.value)
    # клавиатура
    text = 'Сколько позиций рейтинга прислать?'
    await cb.message.answer(text, reply_markup=kb.get_len_rating_kb())


# рейтинг
# @dp.message(StateFilter(Callbacks.ADMIN_RATING_START.value))
@dp.callback_query(lambda cb: cb.data.startswith(Callbacks.ADMIN_RATING_SEND.value))
async def admin_rating_send(cb: CallbackQuery, state: FSMContext) -> None:
    _, len_rating_str = cb.data.split(':')
    users_rating = await db.get_users_rating (limit=int(len_rating_str))
    for row in users_rating:
        user_info = await db.get_user_info (row.referrer)
        text = f'{user_info.full_name} - {row.points} подписчиков'
        for admin_id in ADMINS:
            await bot.send_message(
                chat_id=admin_id,
                text=text,
                reply_markup=kb.get_send_message_kb(user_info.user_id))


@dp.callback_query(lambda cb: cb.data.startswith(Callbacks.ADMIN_SEND_MESSAGE.value))
async def admin_rating_start(cb: CallbackQuery, state: FSMContext):
    _, user_id = cb.data.split(':')

    await state.set_state(Callbacks.ADMIN_SEND_MESSAGE.value)

    if user_id == 'all':
        text = '❕ Сообщение будет отправлено всем пользователям'
    else:
        user_info = await db.get_user_info (user_id)
        text = f'❕ Сообщение будет отправлено пользователю {user_info.full_name}'

    sent = await cb.message.answer(text, reply_markup=kb.get_close_kb())
    await state.update_data (data={
        'user_id': user_id,
        'message_id': sent.message_id,
        'text': sent.text,
        'entities': sent.entities
    })


# написать по...
@dp.callback_query(lambda cb: cb.data.startswith(Callbacks.ADMIN_SEARCH_USER.value))
async def admin_rating_start(cb: CallbackQuery, state: FSMContext):
    _, pattern = cb.data.split(':')

    await state.set_state(Callbacks.ADMIN_SEARCH_USER.value)
    await state.update_data(data={'pattern': pattern})

    if pattern == 'id':
        pattern_str = 'ID'
    elif pattern == 'fullname':
        pattern_str = 'полное имя'
    else:
        pattern_str = 'имя пользователя'

    text = f'Отправьте {pattern_str} пользователя'
    await cb.message.answer(text=text, reply_markup=kb.get_close_kb())


# рейтинг
@dp.message(StateFilter(Callbacks.ADMIN_SEARCH_USER.value))
async def admin_rating_send(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()

    print(msg.text)
    print(data['pattern'])

    if data['pattern'] == 'id':
        print ('id')
        user_info = await db.search_user(user_id=msg.text)
    elif data['pattern'] == 'fullname':
        print ('fullname')
        user_info = await db.search_user(full_name=msg.text)
    else:
        print ('username')
        user_info = await db.search_user(username=msg.text)

    if user_info:
        await state.clear ()
        text = f'{user_info.user_id} {user_info.full_name} {user_info.username}'
        await msg.answer(text=text, reply_markup=kb.get_send_message_kb(user_info.user_id))

    else:
        sent = await msg.answer(f'❗️ Пользователь {msg.text} не найден')
        await sleep(3)
        await sent.delete()


# рейтинг
@dp.message(StateFilter(Callbacks.ADMIN_SEND_MESSAGE.value))
async def admin_rating_send(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()

    if data['user_id'] == 'all':
        users = await db.get_all_users_info()

    else:
        user = await db.get_user_info(data ['user_id'])
        users = (user, )

    counter = 0
    for user in users:
        try:
            if msg.content_type == ContentType.TEXT:
                await bot.send_message(chat_id=user.user_id, text=msg.text, entities=msg.entities, parse_mode=None)

            elif msg.content_type == ContentType.PHOTO:
                await bot.send_photo(
                    chat_id=user.user_id,
                    photo=msg.photo[-1].file_id,
                    caption=msg.caption,
                    caption_entities=msg.caption_entities,
                    parse_mode=None
                )

            elif msg.content_type == ContentType.VIDEO:
                await bot.send_video (
                    chat_id=user.user_id,
                    video=msg.video.file_id,
                    caption=msg.caption,
                    caption_entities=msg.caption_entities,
                    parse_mode=None
                )

            elif msg.content_type == ContentType.VIDEO_NOTE:
                await bot.send_video_note (
                    chat_id=user.user_id,
                    video_note=msg.video_note.file_id,
                )

            elif msg.content_type == ContentType.VOICE:
                await bot.send_voice (
                    chat_id=user.user_id,
                    voice=msg.voice.file_id,
                )

            elif msg.content_type == ContentType.ANIMATION:
                await bot.send_animation (
                    chat_id=user.user_id,
                    animation=msg.animation.file_id,
                    caption=msg.caption,
                    caption_entities=msg.caption_entities,
                    parse_mode=None
                )

            else:
                await msg.answer('❌ Ни одно сообщение не отправлено. Неподдерживаемый формат сообщения')
                break

            counter += 1
        except Exception as ex:
            print(ex)
            pass

    if data ['user_id'] == 'all':
        end_text = f'✅ Сообщение отправлено {counter} пользователям'
    else:
        end_text = f'✅ Сообщение отправлено'

    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=data['message_id'],
        text=f"{data['text']}\n\n{end_text}",
        entities=data['entities'],
    )
