Yatube API
Описание

Yatube API — это серверная часть социальной сети для публикации личных дневников (постов). API предоставляет интерфейс для создания, чтения, обновления и удаления постов, комментариев, групп и подписок. Реализована аутентификация пользователей с помощью JWT-токенов.
Технологии

    Python 3.7+

    Django 3.2

    Django REST Framework

    djangorestframework-simplejwt

    pytest

    SQLite (для разработки)

Установка и запуск

    Клонируйте репозиторий:
    Выполните команду git clone <адрес_репозитория>, затем перейдите в папку проекта с помощью cd <название_папки_с_проектом>.

    Создайте и активируйте виртуальное окружение:
    Для создания виртуального окружения выполните команду python3 -m venv venv. Для активации используйте:

        На Linux/macOS: source venv/bin/activate

        На Windows: venv\Scripts\activate

    Установите зависимости:
    Выполните команду pip install -r requirements.txt, чтобы установить все необходимые зависимости.

    Выполните миграции:
    Запустите команду python manage.py migrate, чтобы применить миграции к базе данных.

    Создайте суперпользователя:
    Выполните команду python manage.py createsuperuser, чтобы создать учетную запись администратора.

    Запустите сервер:
    Запустите сервер с помощью команды python manage.py runserver. Сервер будет доступен по адресу http://127.0.0.1:8000/. Документация API (Redoc) доступна по адресу http://127.0.0.1:8000/redoc/.

Примеры запросов

Для выполнения запросов к API вам потребуется получить JWT-токен.
Получение JWT-токена

Отправьте POST-запрос на эндпоинт /api/v1/jwt/create/ с телом запроса в формате JSON, содержащим ваш username и пароль. Пример тела запроса:

{
"username": "<ваш_username>",
"password": "<ваш_пароль>"
}

В ответ вы получите JSON с refresh- и access-токенами. Пример ответа:

{
"refresh": "<refresh_token>",
"access": "<access_token>"
}

Полученный access_token нужно использовать в заголовке Authorization последующих запросов. Пример заголовка:

Authorization: Bearer <access_token>
Создание поста

Отправьте POST-запрос на эндпоинт /api/v1/posts/ с телом запроса в формате JSON. Пример тела запроса:

{
"text": "Текст моего поста.",
"group": null
}
Получение списка постов

Отправьте GET-запрос на эндпоинт /api/v1/posts/, чтобы получить список всех постов.
Получение списка постов с пагинацией

Отправьте GET-запрос на эндпоинт /api/v1/posts/ с параметрами limit и offset. Например, /api/v1/posts/?limit=2&offset=1.
Получение списка групп

Отправьте GET-запрос на эндпоинт /api/v1/groups/, чтобы получить список всех групп.
Получение списка подписок

Отправьте GET-запрос на эндпоинт /api/v1/follow/, чтобы получить список подписок. Этот запрос доступен только для авторизованных пользователей.
Создание подписки

Отправьте POST-запрос на эндпоинт /api/v1/follow/ с телом запроса в формате JSON. Пример тела запроса:

{
"following": "<username_пользователя>"
}

Этот запрос доступен только для авторизованных пользователей.
Получение списка комментариев к посту

Отправьте GET-запрос на эндпоинт /api/v1/posts/{post_id}/comments/, чтобы получить список комментариев к конкретному посту. Например, /api/v1/posts/1/comments/. Этот запрос доступен только для авторизованных пользователей.
Создание комментария

Отправьте POST-запрос на эндпоинт /api/v1/posts/{post_id}/comments/ с телом запроса в формате JSON. Пример тела запроса:

{
"text": "Текст комментария."
}

Например, /api/v1/posts/1/comments/. Этот запрос доступен только для авторизованных пользователей.

Важно: Не забудьте заменить <адрес_репозитория>, <название_папки_с_проектом>, <ваш_username> и <ваш_пароль> на свои значения.