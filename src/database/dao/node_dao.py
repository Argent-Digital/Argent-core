from sqlalchemy import select
from src.database.database import async_session_factory
from src.database.models import NodesOrm

class NodesDao:

    @classmethod 
    async def node_by_id(cls, node_id: int):
        async with async_session_factory() as session:
            query = (
                select(NodesOrm)
                .where(NodesOrm.id == node_id)
            )
            res = await session.execute(query)
            return res.scalar_one_or_none()
        
    @classmethod
    async def select_nodes_list(cls):
        async with async_session_factory() as session:
            stmt = select(NodesOrm)
            res = await session.execute(stmt)
            return res.scalars().all()