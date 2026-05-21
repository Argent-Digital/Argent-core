from sqlalchemy import Table, Column, Integer, String, ForeignKey, text, BigInteger, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from typing import Annotated, List
import uuid
import datetime

intpk = Annotated[int, mapped_column(BigInteger, primary_key=True)]

class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None]
    first_name: Mapped[str]
    balance: Mapped[int] = mapped_column(server_default="0")
    referrer_id: Mapped[int | None] = mapped_column(BigInteger)
    registration_date: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )
    is_verified: Mapped[bool] = mapped_column(server_default=text("'false'"))

    key: Mapped["VpnKeysOrm"] = relationship(back_populates="user", uselist=False)

class VpnKeysOrm(Base):
    __tablename__ = "vpn_keys"

    key_id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), unique=True)
    server_key_id: Mapped[str | None]
    key_name: Mapped[str]
    access_url: Mapped[str]
    is_active: Mapped[bool] = mapped_column(server_default=text("'true'"))
    expiry_date: Mapped[datetime.datetime | None]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    protocol: Mapped[str] = mapped_column(server_default=text("'outline'"))
    vless_uuid: Mapped[uuid.UUID | None] = mapped_column(UUID, nullable=True)

    user: Mapped["UsersOrm"] = relationship(back_populates="key")

    nodes_id: Mapped[int | None] = mapped_column(ForeignKey("nodes.id"))
    node: Mapped["NodesOrm"] = relationship(back_populates="keys")

class NodesOrm(Base):
    __tablename__ = "nodes"

    id: Mapped[intpk] = mapped_column(primary_key=True)
    name: Mapped[str]
    country: Mapped[str]
    ip: Mapped[str]

    ux_username: Mapped[str]
    ux_pass: Mapped[str]
    ux_url: Mapped[str]

    out_url: Mapped[str]
    out_cert: Mapped[str]

    allow_new_key: Mapped[bool] = mapped_column(server_default=text("'true'"))
    keys: Mapped[List["VpnKeysOrm"]] = relationship(back_populates="node")