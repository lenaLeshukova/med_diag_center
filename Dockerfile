FROM python:3.12-slim

# Установка системных зависимостей для сборки psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Устанавливаем poetry внутри контейнера
RUN pip install --no-cache-dir poetry

# Отключаем создание виртуальных окружений внутри контейнера (в докере это не нужно)
RUN poetry config virtualenvs.create false

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем продакшн-зависимости
RUN poetry install --no-root --only main

# Копируем весь остальной код проекта
COPY . /app/

# Открываем порт для Django
EXPOSE 8000

# Команда для запуска (соберем статику, применим миграции и запустим сервер)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
