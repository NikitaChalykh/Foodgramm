FoodGramm
![example workflow](https://github.com/NikitaChalykh/foodgram-project-react/actions/workflows/foodgramm_workflow.yml/badge.svg)
=====

Описание проекта
----------
Cайт Foodgram («Продуктовый помощник») создан для начинающих кулинаров и изысканныю гурманов.

[Ссылка на размещенный проект на боевом сервере](http://chafoodgramm.ddns.net/)

Логин администратора: ```admin```

Пароль администратора: ```admin```

Системные требования
----------
* Python 3.7+
* Docker
* Works on Linux, Windows, macOS, BSD

Стек технологий
----------
* Python 3.7
* Django 2.2
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
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py collectstatic --no-input 

docker-compose exec web python manage.py loaddata fixtures.json
```
