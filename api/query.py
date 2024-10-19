from .db import Trivia
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import random


async def get_random_id(session: AsyncSession) -> int:
    stmt = select(func.max(Trivia.id))
    result = await session.execute(stmt)
    count = result.scalar()
    return random.randint(1, count)


async def get_random_trivia(session: AsyncSession) -> Trivia:   
    random_id = await get_random_id(session)
    # Get row by id
    stmt = select(Trivia).where(Trivia.id == random_id)
    result = await session.execute(stmt)
    return result.scalar()


async def get_trivia_by_id(session: AsyncSession, question_id: int) -> Trivia:
    stmt = select(Trivia).where(Trivia.id == question_id)
    result = await session.execute(stmt)
    return result.scalar()