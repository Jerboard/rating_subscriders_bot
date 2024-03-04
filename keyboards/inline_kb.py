from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from enums import Callbacks


# кнопка-ссылка на канал
def get_channel_link_kb(link: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Перейти в канал', url=link)]
    ])


# оснавная клавиатура админов
def get_main_admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Статистика', callback_data=Callbacks.ADMIN_STATISTIC.value)],
        [InlineKeyboardButton(text='Написать лидерам рейтинга', callback_data=Callbacks.ADMIN_RATING_START.value)],
        [InlineKeyboardButton(text='Написать всем', callback_data=f'{Callbacks.ADMIN_SEND_MESSAGE.value}:all')],
    ])


# Написать пользователю
def get_send_message_kb(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Написать', callback_data=f'{Callbacks.ADMIN_SEND_MESSAGE.value}:{user_id}')]
    ])


# Отмена действия
def get_close_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🗑 Отмена', callback_data=Callbacks.CLOSE.value)]
    ])


# количество победителей
def get_len_rating_kb():
    kb = InlineKeyboardBuilder()
    for i in range(1, 21):
        kb.button(text=f'{i}', callback_data=f'{Callbacks.ADMIN_RATING_SEND.value}:{i}')
    kb.button(text='🗑 Отмена', callback_data=Callbacks.CLOSE.value)
    return kb.adjust(5, 5, 5, 5, 1).as_markup()

