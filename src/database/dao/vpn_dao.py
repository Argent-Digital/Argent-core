from sqlalchemy import insert, select, UUID, delete, func
from sqlalchemy.dialects.postgresql import insert
import uuid
from src.database.database import async_session_factory
from src.database.models import VpnKeysOrm, UsersOrm, Nodes

class VpnKeyDao:

    @classmethod
    async def add_vpn_key(
        cls, 
        user_id: int,
        key_name: str,
        access_url: str,
        node_id: int,
        protocol: str = "outline",
        server_key_id: str | None = None,
        vless_uuid: uuid.UUID | None = None
    ):
        async with async_session_factory() as session:
            stmt = (
                insert(VpnKeysOrm)
                .values(
                    user_id = user_id,
                    server_key_id = server_key_id,
                    key_name = key_name,
                    access_url = access_url, 
                    protocol = protocol,
                    vless_uuid = vless_uuid,
                    node_id = node_id
                )
                .on_conflict_do_update(
                    index_elements=['user_id'],
                    set_={
                        'server_key_id': server_key_id,
                        'key_name': key_name,
                        'access_url': access_url,
                        "protocol": protocol,
                        "vless_uuid": vless_uuid
                    }
                )
            )

            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_user_access_url(cls, user_id: int):
        async with async_session_factory() as session:
            stmt = (
                select(VpnKeysOrm)
                .where(VpnKeysOrm.user_id == user_id)
            )
            res = await session.execute(stmt)
            return res.scalar_one_or_none()

    @classmethod
    async def get_user_vpn_data(cls, user_id: int):
        async with async_session_factory() as session:
            stmt = (
                select(VpnKeysOrm)
                .where(VpnKeysOrm.user_id == user_id)
            )
            res = await session.execute(stmt)
            return res.scalar_one_or_none()
        
    @classmethod
    async def get_all_vpn_keys(cls) -> list[VpnKeysOrm]:
        async with async_session_factory() as session:
            stmt = (
                select(VpnKeysOrm)
            )
            res = await session.execute(stmt)
            return res.scalars().all()
        
    @classmethod 
    async def delete_vpn_key(cls, user_id: int):
        async with async_session_factory() as session:
            stmt = (
                delete(VpnKeysOrm)
                .where(VpnKeysOrm.user_id == user_id)
            )
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def billing_clining_keys(cls):
        async with async_session_factory() as session:
            query = (
                select(VpnKeysOrm)
                .join(UsersOrm, UsersOrm.user_id == VpnKeysOrm.user_id)
                .where(UsersOrm.balance < 2)
            )

            result = await session.execute(query)
            keys_to_del = result.scalars().all()

            if not keys_to_del:
                return []
            
            deleted_data = [
                {
                    "user_id": k.user_id,
                    "server_key_id": k.server_key_id,
                    "protocol": k.protocol,
                    "vless_uuid": k.vless_uuid
                } for k in keys_to_del
            ]
            
            delete_stmt = (
                delete(VpnKeysOrm)
                .where(VpnKeysOrm.user_id.in_([k.user_id for k in keys_to_del]))
            )

            await session.execute(delete_stmt)
            await session.commit()
            return deleted_data
        
    @classmethod
    async def optimized_select_nodes(cls):
        async with async_session_factory() as session:
            stmt = (
                select(Nodes)
                .outerjoin(Nodes.keys)
                .where(Nodes.is_active == True)
                .group_by(Nodes.id)
                .order_by(func.count(VpnKeysOrm.key_id).asc())
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()