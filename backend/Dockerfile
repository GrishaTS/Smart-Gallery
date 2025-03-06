FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

COPY . .

ENTRYPOINT ["sh", "-c", "uvicorn app.main:app --host ${BACKEND_HOST} --port ${BACKEND_PORT} --reload"]
