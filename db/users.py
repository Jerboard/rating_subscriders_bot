import sqlalchemy as sa
import typing as t

from datetime import date, datetime

from init import TZ
from db.base import METADATA, begin_connection
from enums import UsersStatus


class UserRow(t.Protocol):
    id: int
    user_id: int
    full_name: str
    username: str
    status: str
    phone_number: str
    invite_link: str
    referrer: int
    get_link_time: datetime
    is_subscriber: bool


class RatingRow(t.Protocol):
    referrer: int
    points: int


UserTable = sa.Table(
    'users',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('user_id', sa.BigInteger),
    sa.Column('full_name', sa.String(255)),
    sa.Column('username', sa.String(255)),
    sa.Column('status', sa.String(255), default='new'),
    sa.Column('invite_link', sa.String(255)),
    sa.Column('phone_number', sa.String(255)),
    sa.Column('referrer', sa.BigInteger),
    sa.Column('is_subscriber', sa.Boolean),
    sa.Column('get_link_time', sa.DateTime(timezone=True))
)


# добавляет пользователя
async def add_user(user_id: int, full_name: str, username: str, referrer: int) -> None:
    query = UserTable.insert().values(user_id=user_id, full_name=full_name, username=username, referrer=referrer)
    async with begin_connection() as conn:
        await conn.execute (query)


# возвращает информацию пользователя
async def get_user_info(user_id: int) -> t.Union[UserRow, None]:
    async with begin_connection() as conn:
        result = await conn.execute(
            UserTable.select().where(UserTable.c.user_id == user_id)
        )
    return result.first()


# возвращает всех пользователей
async def get_all_users_info() -> tuple[UserRow]:
    async with begin_connection() as conn:
        result = await conn.execute(
            UserTable.select()
        )
    return result.all()


# обновляет данные пользователя
async def update_user(
        user_id: int,
        status: str = None,
        invite_link: str = None,
        phone_number: str = None,
        is_subscriber: bool = None,
        get_link_time: datetime = None
) -> None:
    query = UserTable.update().where(UserTable.c.user_id == user_id)

    if status:
        query = query.values(status=status)
    if invite_link:
        query = query.values(invite_link=invite_link)
    if phone_number:
        query = query.values(phone_number=phone_number)
    if get_link_time:
        query = query.values(get_link_time=get_link_time)
    if is_subscriber is not None:
        query = query.values(is_subscriber=is_subscriber)

    async with begin_connection() as conn:
        await conn.execute (query)


# возвращает всех ожидающих подписку
async def get_new_subscribers() -> tuple[UserRow]:
    async with begin_connection() as conn:
        result = await conn.execute (UserTable.select().where(
            sa.or_(
                UserTable.c.status == UsersStatus.GET_LINK.value,
                UserTable.c.status == UsersStatus.GET_LINK_1.value,
                UserTable.c.status == UsersStatus.GET_LINK_3.value,
                UserTable.c.status == UsersStatus.GET_LINK_DAY.value,
                UserTable.c.status == UsersStatus.GET_LINK_DAY_HOUR.value,
            )
        ))

    return result.all()


# возвращает всех подписчиков пользователя
async def get_user_referrals(user_id: int) -> tuple[UserRow]:
    async with begin_connection() as conn:
        result = await conn.execute (
            UserTable.select().where(UserTable.c.referrer == user_id))
                                     # UserTable.c.status != UsersStatus.GET_LINK.value))

    return result.all()


# возвращает рейтинг пользователей
async def get_users_rating(limit: int = 50) -> tuple[RatingRow]:
    query = (UserTable.select().with_only_columns(
        UserTable.c.referrer,
        sa.func.count(UserTable.c.id).label('points')
    ).where(sa.or_(
        UserTable.c.status == UsersStatus.SUBSCRIBER,
        UserTable.c.status == UsersStatus.PARTICIPANT,
        UserTable.c.referrer is not None,
    )).where(UserTable.c.referrer.isnot(None)).
             group_by(UserTable.c.referrer).order_by(sa.desc('points')))

    async with begin_connection() as conn:
        result = await conn.execute (query)

    return result.all()


# возвращает всех подписчиков пользователя
async def get_all_participant() -> tuple[UserRow]:
    async with begin_connection() as conn:
        result = await conn.execute (
            UserTable.select().where(
                UserTable.c.invite_link is not None,
            ).where(sa.or_(
                UserTable.c.status == UsersStatus.SUBSCRIBER,
                UserTable.c.status == UsersStatus.PARTICIPANT,)))

    return result.all()


# возвращает всех подписчиков пользователя
async def get_all_subscriber() -> tuple[UserRow]:
    async with begin_connection() as conn:
        result = await conn.execute (
            UserTable.select().where(
                UserTable.c.referrer is not None,
            ).where(sa.or_(
                UserTable.c.status == UsersStatus.SUBSCRIBER,
                UserTable.c.status == UsersStatus.PARTICIPANT,)))

    return result.all()