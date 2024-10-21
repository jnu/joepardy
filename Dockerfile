FROM node:22.10-bookworm AS webbuild

WORKDIR /code

RUN npm install -g pnpm

WORKDIR /code
COPY web/package.json web/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

ARG node_env=production

COPY ./web/src ./src
COPY ./web/static ./static
COPY web/postcss.config.js web/svelte.config.js web/tailwind.config.js web/tsconfig.json web/vite.config.ts ./
RUN pnpm build -d


FROM python:3.13.0-bookworm AS srv

ENV PYTHONFAULTHANDLER=1 \
      PYTHONUNBUFFERED=1 \
      PYTHONHASHSEED=random \
      PIP_NO_CACHE_DIR=off \
      PIP_DISABLE_PIP_VERSION_CHECK=on \
      PIP_DEFAULT_TIMEOUT=100 \
      POETRY_VIRTUALENVS_CREATE=false

# Set up poetry
RUN pip install poetry==1.8.3

WORKDIR /srv

COPY poetry.lock pyproject.toml /srv/
RUN poetry install --no-interaction --no-ansi --no-root

COPY --from=webbuild /code/build /srv/web/build

COPY ./api /srv/api
COPY ./data /srv/data

CMD ["poetry", "run", "fastapi", "run", "api"]