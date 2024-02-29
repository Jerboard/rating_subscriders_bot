import enum


class ButtonText(str, enum.Enum):
    GET_LINK = 'Получить ссылку'
    SEND_CONTACT = 'Поделиться контактом'


class UsersStatus(str, enum.Enum):
    NEW = 'new'
    GET_LINK = 'get_link'
    PARTICIPANT = 'participant'
    SUBSCRIBER = 'subscriber'
    BLOCKED_BOT = 'blocked_bot'


class Callbacks(str, enum.Enum):
    CLOSE = 'close'
    ADMIN_STATISTIC = 'admin_statistic'
    ADMIN_RATING_START = 'admin_rating_start'
    ADMIN_RATING_SEND = 'admin_rating_send'
    ADMIN_SENDING_ALL = 'admin_sending_all'
    ADMIN_SEND_MESSAGE = 'admin_send_message'
