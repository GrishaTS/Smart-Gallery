# Используем официальный образ Python
FROM python:3.11.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# Копируем файлы зависимостей
COPY backend/pyproject.toml backend/poetry.lock ./

# Устанавливаем зависимости через Poetry (без виртуального окружения)
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

# Копируем остальной код
COPY backend/ .  

# Запускаем приложение
CMD ["python", "main.py"]
