from sqlalchemy import select, func
from src.database.database import async_session_factory
from src.database.models import UsersOrm, VpnKeysOrm
from src.schemas.bot_schema import StatsResponse

class AdminDao:

    @classmethod 
    async def get_stats(cls):
        async with async_session_factory() as session:
            user_query = select(func.count(UsersOrm.id))
            key_query = select(func.count(VpnKeysOrm.key_id))

            users_res = await session.execute(user_query)
            key_res = await session.execute(key_query)

            return StatsResponse(users=users_res.scalar(), keys=key_res.scalar())


