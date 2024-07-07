# requests.py
from app.database.models import async_session
from app.database.models import async_session, User, Message
from sqlalchemy import select, update, delete, desc
import logging


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def add_message(tg_id: int, content: str, role: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            message = Message(user_id=user.id, content=content, role=role)
            session.add(message)
            await session.commit()
            logging.info(f"Added message for user {tg_id}: {role} - {content[:50]}...")
        else:
            logging.error(f"User with tg_id {tg_id} not found")

async def get_chat_history(tg_id: int, limit: int = 10):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            query = select(Message).where(Message.user_id == user.id).order_by(Message.timestamp.desc()).limit(limit)
            result = await session.execute(query)
            messages = result.scalars().all()
            return [(msg.role, msg.content) for msg in reversed(messages)]
    return []

async def clear_chat_history(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            await session.execute(delete(Message).where(Message.user_id == user.id))
            await session.commit()
            return True
    return False