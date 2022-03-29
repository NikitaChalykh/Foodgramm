FoodGram
=====

Описание проекта
----------
Cайт Foodgram («Продуктовый помощник») создан для начинающих кулинаров и изысканныю гурманов.

Проект подготовлен для первичного ревью. В репозитории расположены 
фикстуры для заполнения БД и папка media/ - в ней лежат картинки рецептов. 

На данном этапе в настройках Django установлен ```DEBUG = True``` для раздачи медиа через тестовый сервер.

Системные требования
----------
* Python 3.8+
* Works on Linux, Windows, macOS, BSD

Стек технологий
----------
* Python 3.8
* Django 2.2 
* Rest API
* SQLite3 (на этапе деплоя в качетстве БД будет использован PostgreSQL)
* JS

Установка проекта из репозитория (Linux и macOS)
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone 'git@github.com:NikitaChalykh/foodgram-project-react.git'

cd foodgram-project-react
```
2. Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv env

source env/bin/activate
```
3. Установить зависимости из файла ```requirements.txt```:
```bash
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```
4. Выполнить миграции:
```bash
cd backend

python3 manage.py migrate
```
5. Заполнение БД тестовыми данными:
```bash
python3 manage.py loaddata fixtures.json
```
6. Запустить проект (в режиме сервера Django):
```bash
python3 manage.py runserver
```
7. Запустить контейнер фронтенда:
```bash
cd ../infra

docker-compose up -d
```
