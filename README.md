# API приложение для сервиса приема пожертвований QR-Кот && QRkot_spreadseets.

Это проект, написанный на FastAPI, представляет собой API-интерфейс для сервиса приема пожертвований QR-Кот.
Основные функции:
* Создание проектов для сбора пожертвований.
* Создание пожертвований.
* Создание отчета о самых быстрых по сбору средств проектах.

Жртвоввать и просматривать список доступных проектов может каждый пользователь.
Зарегестрированный пользователь может просматривать историю своих пожертвований.
Суперпользователю доступна максимальная информация.

Удалять пользователей нельзя, можно только сделать их неактивными.

Суперпользователь может вносить изменения в проект, но с ограничениями:
* Нельзя удалять закрытые проекты и проекты в которые уже были сделаны пожертвования
* Нельзя коррекировать требуемую сумму в меньшую сторону.

# Стэк технологий.

FastAPI, SQLAlchemi, MySQL, Alembic, Dependency Injector, Uvicorn, Aiogoogle

# Пример файла с переменными окружения

.env.example

# Документация OpenAPI

После запуска проекта документация OpenAPI будет надохится по адресу
http://127.0.0.1:8000/docs

# Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

# Команды для применения миграций Alembic

Усли Alembic еще не запущен в проекте, то его надо инициировать
```
alembic init --template async alembic
```
Для создания файла миграций используйте
```
alembic revision -m "Ваш комментарий."
```
Для проведения миграций
```
alembic upgrade head
```

# Запуск проекта из корневой директории
```
uvicorn app.main:app
```