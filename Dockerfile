# syntax = docker/dockerfile:1.4.0
FROM python:3.11-slim-bookworm as operating-system-deps
WORKDIR /app

# Keeps Python from generating .pyc files in the container
# Turns off buffering for easier container logging
# Force UTF8 encoding for funky character handling
# Needed so imports function properly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
ENV PYTHONPATH=/app
# Keep the venv name and location predictable
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
# Control the number of workers Gunicorn uses
ENV WEB_CONCURRENCY=1

# "Activate" the venv manually for the context of the container
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential=* \
  libpq-dev=* && \
  rm -rf /var/lib/apt/lists/*

FROM operating-system-deps
ARG app
ARG port=80

COPY ./${app}/pyproject.toml ./${app}/poetry.lock /app/
RUN pip install --no-cache-dir poetry==1.5.1 && \
  poetry install

COPY ./.openapi /app/.openapi
COPY ${app} ./${app}

# use a RUN to create an entrypoint because the ENTRYPOINT directive does not
# support variable substitution
RUN <<EOF cat >> /app/entrypoint.sh && chmod +x /app/entrypoint.sh
#!/usr/bin/env bash
gunicorn -b 0.0.0.0:${port} -t 240 --preload "provider:create_app()"
EOF

WORKDIR /app/${app}
EXPOSE ${port}
ENTRYPOINT ["/app/entrypoint.sh"]