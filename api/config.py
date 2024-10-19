from pydantic import BaseModel
from glowplug import SqliteSettings
from .llm import OpenAIChatSettings, LlmSettings
import os


class StaticAssetsSettings(BaseModel):
    directory: str = os.path.join("web", "build")
    index: str = "index.html"

    @property
    def index_file(self):
        return os.path.join(self.directory, self.index)

class Config(BaseModel):
    db: SqliteSettings = SqliteSettings(engine="sqlite", path=os.path.join("data", "trivia.db"))
    llm: LlmSettings = OpenAIChatSettings()
    assets: StaticAssetsSettings = StaticAssetsSettings()


config = Config()