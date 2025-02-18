FROM python:3.12-alpine

WORKDIR /frontend

# Установка зависимостей для Flet
RUN apk add --no-cache \
    gtk+3.0 \
    libx11 \
    gstreamer \
    gst-plugins-good \
    gst-plugins-bad \
    gst-plugins-base \
    ffmpeg \
    bash \
    libmagic

# Создание виртуального окружения
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Установка Python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Запуск приложения
CMD ["python", "app/main.py"]