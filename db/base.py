import typing as t
import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncConnection

from init import ENGINE

METADATA = sa.MetaData ()


def begin_connection() -> t.AsyncContextManager [AsyncConnection]:
    conn = ENGINE.begin ()
    if not conn:
        ENGINE.connect()
        return ENGINE.begin
    return conn
    # return ENGINE.begin ()


async def init_models():
    async with ENGINE.begin () as conn:
        await conn.run_sync (METADATA.create_all)