FROM python:3.11-slim AS builder

WORKDIR /app
ENV PYTHONPATH=/app/src

RUN pip install --no-cache-dir "poetry==1.8.2"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-interaction --no-ansi

COPY src/ ./src/


FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /usr/sbin/nologin appuser

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/src /app/src
COPY --from=builder /app/pyproject.toml /app/poetry.lock /app/

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
