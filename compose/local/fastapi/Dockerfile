FROM python:3.13.11-slim-trixie AS builder

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --no-install-project

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen

FROM python:3.13.11-slim-trixie AS runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
  libpq5 \
  telnet netcat-openbsd \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/*

COPY ./compose/local/fastapi/entrypoint.sh /entrypoint.sh
COPY ./compose/local/fastapi/start.sh /start.sh
COPY ./compose/local/fastapi/celery/worker/start.sh /start-celeryworker.sh
COPY ./compose/local/fastapi/celery/beat/start.sh /start-celerybeat.sh
COPY ./compose/local/fastapi/celery/flower/start.sh /start-flower.sh

RUN sed -i 's/\r$//g' /entrypoint.sh /start.sh /start-celeryworker.sh /start-celerybeat.sh /start-flower.sh && \
  chmod +x /entrypoint.sh /start.sh /start-celeryworker.sh /start-celerybeat.sh /start-flower.sh

ENTRYPOINT ["/entrypoint.sh"]

