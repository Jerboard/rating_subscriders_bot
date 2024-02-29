from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from enums import ButtonText


# дай кнопку участвовать
def get_start_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text=ButtonText.GET_LINK.value)]
    ])


# дай кнопку отправить контакт
def get_send_contact_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text=ButtonText.SEND_CONTACT.value, request_contact=True)]
    ])
