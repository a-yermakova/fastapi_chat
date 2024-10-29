## Сервис обмена мгновенными сообщениями

Чат c использованием протоколов HTTP и WebSocket и интеграцией с Telegram-ботом для отправки уведомлений

#### Инструкция по использованию:

- Регистрация на [сайте](https://perfect-joey-eager.ngrok-free.app) через форму Sign Up
- В телеграм найти бота @ya_sample_bot 
- Отправить команду /start, затем /register, ввести данные зарегистрированного аккаунта
- Войти в чат через форму Sign In
- Отправлять сообщения

### API

**Полная документация: [Swagger](https://perfect-joey-eager.ngrok-free.app/docs)**

#### Доступен следующий функционал:

- Регистрация
- Авторизация
- Выход из учетной записи
- Получение всех доступных для отправки сообщения пользователей
- Получение истории сообщений с выбранным пользователем
- Отправка сообщения выбранному пользователю
- Подключение по WebSocket для ожидания новых сообщений от выбранного пользователя


### Установка

#### Предварительные требования

- Docker и Docker Compose установлены.
- API токен для Telegram-бота.

#### Шаги установки

- Клонируйте репозиторий

```bash
    git clone https://github.com/a-yermakova/fastapi_chat.git
    cd <имя директории>
```
- Создайте файл `.env-non-dev`

В корне проекта создайте файл `.env-non-dev` со следующими переменными:

```plaintext
    TELEGRAM_TOKEN=your-telegram-api-token

    DB_HOST=db
    DB_PORT=5432
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASS=postgres

    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres

    REDIS_HOST=redis
    REDIS_PORT=6379

    SECRET_KEY=your-secret-key
```

- Соберите и запустите Docker-контейнер

```bash
    docker-compose up --build
```    
### Стек технологий

**Backend:** Python (FastAPI), SQLAlchemy, PostgreSQL, Redis, Celery, Docker, Nginx, Aiogram (Telegram Bot API)

**Frontend:**  HTML, CSS, JavaScript

