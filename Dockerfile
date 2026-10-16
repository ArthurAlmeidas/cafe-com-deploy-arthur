FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

FROM base AS deps
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM base AS runtime
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
COPY --from=deps /install /usr/local
RUN useradd --create-home appuser
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8000
HEALTHCHECK --start-period=30s CMD sh -c "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8000}/health')\""
# roda as migrations e sobe a API
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
