# Используем базовый образ Python
FROM python:3.11-alpine

# Устанавливаем postgresql-client через apk
RUN apk update && apk add --no-cache postgresql-client

# Установка зависимостей для PostgreSQL и других пакетов
RUN apk add --no-cache postgresql-dev gcc musl-dev libffi-dev

# Рабочая директория
WORKDIR /usr/src/app

# Создание директорий для статических и медиафайлов
RUN mkdir -p static media

# Переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Обновим pip
RUN pip install --upgrade pip

# Скопируем файл с зависимостями и установим их
COPY ./requirements.txt ./
RUN pip install -r requirements.txt --verbose


# Скопируем оставшиеся файлы проекта
COPY . .

# Проверка наличия manage.py
RUN ls -la /usr/src/app/

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
