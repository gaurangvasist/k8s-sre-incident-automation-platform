FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_PORT=8080

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir .

USER app

EXPOSE 8080

CMD ["uvicorn", "sre_ops_health_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
