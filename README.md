FoodGramm
![example workflow](https://github.com/NikitaChalykh/foodgram-project-react/actions/workflows/foodgramm_workflow.yml/badge.svg)
=====

Описание проекта
----------
Cайт Foodgram («Продуктовый помощник») создан для начинающих кулинаров и изысканныю гурманов. В сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект разворачивается в трех Docker контейнерах: backend-приложение API, postgresql-база данных и nginx-сервер на боевом сервере Yandex.Cloud. Контейнер с фронтендом используется только для сборки файлов. Реализовано CI и CD проекта. 

При пуше изменений в главную ветку проект автоматические тестируется на соотвествие требованиям PEP8. После успешного прохождения тестов, на git-платформе собирается образ web-контейнера Docker и автоматически размешается в облачном хранилище DockerHub. Размещенный образ автоматически разворачивается на боевом сервере вмете с контейнером веб-сервера nginx и базой данных PostgreSQL.

[Ссылка на размещенный проект на сервере Yandex.Cloud](http://chafoodgramm.ddns.net/)

Системные требования
----------
* Python 3.7+
* Docker
* Works on Linux, Windows, macOS, BSD

Стек технологий
----------
* Python 3.7
* Django 3.1
* Rest API
* PostgreSQL
* JS
* Nginx
* gunicorn
* Docker
* DockerHub
* GitHub Actions (CI/CD)

Установка проекта из репозитория (Linux и macOS)
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone 'git@github.com:NikitaChalykh/foodgram-project-react.git'

cd foodgram-project-react
```
2. Cоздать и открыть файл ```.env``` с переменными окружения:
```bash 
cd infra

touch .env
```

3. Заполнить ```.env``` файл с переменными окружения по примеру (SECRET_KEY см. в файле ```settnigs.py```):
```bash 
echo DB_ENGINE=django.db.backends.postgresql >> .env

echo DB_NAME=postgres >> .env

echo POSTGRES_PASSWORD=postgres >> .env

echo POSTGRES_USER=postgres >> .env

echo DB_HOST=db >> .env

echo DB_PORT=5432 >> .env

echo SECRET_KEY=************ >> .env
```

4. Установка и запуск приложения в контейнерах (контейнер web загружактся из DockerHub):
```bash 
docker-compose up -d
```

5. Запуск миграций, сбор статики и заполнение БД:
```bash 
docker-compose exec backend python manage.py migrate

docker-compose exec backend python manage.py collectstatic --no-input 

docker-compose exec backend python manage.py loaddata fixtures.json
```
