import openai
from pydantic import BaseModel
from functools import cached_property


_system = """\
You are good at explaining trivia questions clearly and concisely.

I will give you a trivia question and answer that has appeared on Jeopardy, and you will give me more information about it.

You may include interesting and relevant facts about the subject in this response.

Remember to be very focused, clear, and concise.\
"""


class OpenAIChatSettings(BaseModel):
    engine: str = "openai-chat"
    api_key: str | None = None
    model: str = "gpt-4o"
    
    @cached_property
    def driver(self):
        return OpenAIChatDriver(api_key=self.api_key, model=self.model)
    
class OpenAIChatDriver:

    def __init__(self, api_key: str, model: str):
        self.model = model
        kwargs = {}
        if api_key:
            kwargs["api_key"] = api_key
        self.client = openai.AsyncClient(**kwargs)

    async def generate(self, category: str, question: str, answer: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": _system
                },
                {
                    "role": "user",
                    "content": f"Category: {category}\nQ: {question}\nA: {answer}"
                }
            ]
        )
        return response.choices[0].message

LlmSettings = OpenAIChatSettings