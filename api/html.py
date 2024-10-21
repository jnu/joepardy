from fastapi import Request
import os
import re
from urllib.parse import quote_plus
import textwrap
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from .db import Trivia
import logging

logger = logging.getLogger(__name__)


class Index:

    _path: str

    _raw: str

    _tpl_head: str

    _tpl_tail: str

    def __init__(self, index_file: str):
        self._path = index_file
        with open(self._path, "r") as f:
            self._raw = f.read()
        
        # Find the `<head>` tag, we will inject just after it.
        inject_point = self._raw.find("<head>") + len("<head>")
        self._tpl_head = self._raw[:inject_point]
        self._tpl_tail = self._raw[inject_point:]

    async def render(self, request: Request, session: AsyncSession):
        slug, id_ = await self._parse_url(request)
        if not id_:
            return self._raw
        
        # Inject the meta tags into the template.
        trivia = await self._get_trivia(session, id_)
        if not trivia:
            return self._raw
        
        meta = self._format_meta(trivia)
        return self._tpl_head + meta + self._tpl_tail

    def _format_meta(self, trivia: Trivia, base_url: str = "https://placehold.jp/30/60a5fa/ffffff/600x400.png?css=%7B%22padding%22%3A%22%2010px%22%7D&text=", wrap: bool = False) -> str:
        t = quote_plus(trivia.answer)
        if wrap:
            t = "\\n".join([quote_plus(line) for line in textwrap.wrap(trivia.answer, 40)])
        html_escaped = trivia.answer.replace('"', "\\\"")
        url = f"{base_url}{t}"
        return """\
<meta property="og:title" content="Answer #{}">
<meta property="og:description" content="{}">
<meta property="og:image" content="{}">
""".format(trivia.id, html_escaped, url)

    async def _parse_url(self, request: Request) -> tuple[str, int]:
        # The URLs are generally in the format `/explain/:id` or `/trivia/:id`.
        # If they aren't, we can just return the template directly.
        # If they are, we can parse the ID to embed the data.
        path = request.url.path
        match = re.match(r"/(trivia|explain)/(\d+)", path)
        if not match:
            return path, 0
        return match.group(1), int(match.group(2))
    
    async def _get_trivia(self, session: AsyncSession, id_: int):
        try:
            stmt = select(Trivia).where(Trivia.id == id_)
            result = await session.execute(stmt)
            return result.scalar()
        except Exception as e:
            logger.exception(f"Failed to get trivia: {e}")
            return None





_index: Index | None = None

async def render_index(request: Request, index_file: str = "index.html"):
    global _index
    if not _index:
        _index = Index(index_file)

    return await _index.render(request, request.state.db)