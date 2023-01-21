# Проект помощь котам

## Описание проекта:

Приложение для Благотворительного фонда поддержки котиков QRKot. Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале,на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Использовано

    Python 3.9
    FastAPI
    SQLAlchemy
    Google API

## Клонировать репозиторий и перейти в него в командной строке:

    git clone https://github.com/pupersa23/cat_charity_fund.git
    cd cat_charity_fund

## Cоздать и активировать виртуальное окружение:

    python3 -m venv venv

### Если у вас Linux/MacOS

    source venv/bin/activate

### Если у вас windows

    source venv/scripts/activate

### Установить зависимости из файла requirements.txt:

    python3 -m pip install --upgrade pip
    pip install -r requirements.txt

## Создать файл .env с настройками проекта

    APP_TITLE=
    DATABASE_URL= 
    SECRET=

    alembic upgrade head

## Запустить приложение

    uvicorn app.main:app


# Автор

Рязанов Владимир - ryazanov745@gmail.com
