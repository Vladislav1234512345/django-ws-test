**Запуск проекта путем контейнеризации**

1. Собирает образы и запускат контейнер:
docker-compose up --build

2. Вход в корневой каталог контейнера:
docker exec -it django-ws-test-web-1 /bin/sh

3. После входа в корневую папку контейнера, создадим супер-пользователя:
python manage.py createsuperuser



**Инструкция по запуску django проекта с использованием websockets (Windows)**

1. Создание виртуального окружения:
python -m venv venv

2. Активация виртуального окружения:
venv\Scripts\activate

3. Зайти в папку проекта django:
cd django_project

4. Запустить сервер django:
python manage.py runserver

5. Создание нового экземпляра локального терминала

6. Скачивание и запуск redis через docker:
docker run --rm -p 6379:6379 redis:7

