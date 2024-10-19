import fastapi
import logging
from contextlib import asynccontextmanager

from .config import config
import api.query as q

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(api: fastapi.FastAPI):
    """Setup and teardown logic for the server."""
    logger.warning("Starting up ...")

    yield

    logger.info("Bye!")

app = fastapi.FastAPI(lifespan=lifespan)

@app.middleware("http")
async def begin_db_session(request: fastapi.Request, call_next):
    async with config.db.driver.async_session_with_args(
        pool_pre_ping=True
    )() as session:
        request.state.db = session
        try:
            response = await call_next(request)
            await session.commit()
            return response
        except Exception as e:
            await session.rollback()
            raise e

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.get("/api/v1/questions/random")
async def read_random(request: fastapi.Request):
    row = await q.random_trivia(request.state.db)
    return row

@app.get("/api/v1/questions/{question_id}")
async def read_question(request: fastapi.Request, question_id: int):
    row = await q.get_trivia_by_id(request.state.db, question_id)
    return row

@app.get("/api/v1/questions/{question_id}/explain")
async def explain_question(request: fastapi.Request, question_id: int):
    row = await q.get_trivia_by_id(request.state.db, question_id)
    summary = await config.llm.driver.generate(row.category, row.answer, row.question)
    return {
        "trivium": row,
        "summary": summary,
    }