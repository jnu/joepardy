from pydantic import BaseModel
from glowplug import SqliteSettings
from .llm import OpenAIChatSettings, LlmSettings


class Config(BaseModel):
    db: SqliteSettings = SqliteSettings(engine="sqlite", path="data/trivia.db")
    llm: LlmSettings = OpenAIChatSettings()


config = Config()