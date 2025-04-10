FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --fix-missing build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /ml_api

COPY requirements.txt .
RUN pip install --no-cache-dir "pip==23.0.1"
RUN pip install --no-cache-dir Cython wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install huggingface_hub==0.23.3 --force-reinstall --no-deps

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

COPY . .

ENTRYPOINT ["sh", "-c", "uvicorn app.main:app --host ${ML_API_HOST} --port ${ML_API_PORT} --reload"]
