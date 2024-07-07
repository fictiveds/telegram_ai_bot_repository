# models.py
from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime, timezone

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=True)
    
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = 'messages'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    content: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)  # 'user' или 'assistant'
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="messages")

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    messages: Mapped[list["Message"]] = relationship(back_populates="user")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)