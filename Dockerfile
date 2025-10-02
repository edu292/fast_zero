FROM python:3.13-slim AS builder

RUN pip install --upgrade pip & pip install poetry

RUN poetry self add poetry-plugin-export

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry export --output requirements.txt --without-hashes

FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache-dir --no-deps -r requirements.txt

COPY alembic.ini .
COPY fast_zero ./fast_zero
COPY migrations ./migrations

EXPOSE 8000
CMD ["uvicorn", "--host", "0.0.0.0", "fast_zero.app:app"]