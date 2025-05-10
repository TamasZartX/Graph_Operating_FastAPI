FROM python:3.11-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
