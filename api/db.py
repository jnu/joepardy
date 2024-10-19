import logging
import random

from glowplug import DbDriver
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import String
from typing_extensions import Annotated

logger = logging.getLogger(__name__)


str_256 = Annotated[str, 256]
text = Annotated[str, 4096]


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {
        str_256: String(255),
        text: String(8191),
    }


# SQL to create a `trivia` table.
# `id` - primary key, integer.
# `season` - season number, integer.
# `category` - name of the category, string.
# `question` - question text, string.
# `answer` - answer text, string.
# `score` - number of points for the question, integer.
class Trivia(Base):
    __tablename__ = "trivia"

    id: Mapped[int] = mapped_column(primary_key=True)
    season: Mapped[int] = mapped_column()
    category: Mapped[str_256] = mapped_column()
    question: Mapped[text] = mapped_column()
    answer: Mapped[text] = mapped_column()
    score: Mapped[int] = mapped_column()


async def init_db(driver: DbDriver, drop_first: bool = False) -> None:
    """Initialize the database and its tables.

    Args:
        driver (DbDriver): The database driver.
        drop_first (bool): Whether to drop the tables first
    """
    if not await driver.exists():
        logger.info("No database exists, creating a new one")
        await driver.create()
    else:
        logger.info("Database already exists")

    # Create the database
    if drop_first:
        logger.info("Re-creating database tables")
    else:
        logger.info("Creating database tables")
    await driver.init(Base, drop_first=drop_first)
