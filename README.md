# User Management API

REST API для управления пользователями.

Проект реализован на FastAPI с асинхронным доступом к PostgreSQL, JWT-аутентификацией и Redis для ограничения частоты запросов.

Основные возможности:

- регистрация пользователей;
- авторизация через JWT;
- получение списка пользователей с пагинацией;
- защита endpoint через Bearer Token;
- rate limit для регистрации;
- миграции базы данных через Alembic;
- запуск всех сервисов через Docker Compose.


## Технологический стек

- Python 3.14
- FastAPI
- SQLAlchemy Async
- PostgreSQL 17
- Redis 7
- Alembic
- Pydantic Settings
- JWT
- Docker / Docker Compose


## Архитектура проекта

Проект построен по слоистой архитектуре:

```
API
 |
 v
Services
 |
 +--> Repositories ---> PostgreSQL
 |
 +--> Redis
```

Ответственность слоёв:

- **API** — обработка HTTP-запросов;
- **Services** — бизнес-логика;
- **Repositories** — работа с базой данных;
- **Schemas** — контракты API;
- **Core** — безопасность, настройки, исключения;
- **DB** — подключения к внешним сервисам.


Подробнее об архитектуре:

```
ARCHITECTURE.md
```


# Запуск проекта


## Требования

Необходимо установить:

- Docker
- Docker Compose


## Подготовка окружения

Создать файл `.env`:

```bash
cp .env.example .env
```


Пример конфигурации:

```env
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=user_management
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

REDIS_HOST=redis
REDIS_PORT=6379

APP_PORT=8000

JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256

RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW_SECONDS=60
```


## Запуск через Docker Compose

Собрать и запустить контейнеры:

```bash
docker compose up --build
```


После запуска приложение доступно:

```
http://localhost:8000
```


Swagger документация:

```
http://localhost:8000/docs
```


## Сервисы Docker Compose


| Сервис | Назначение |
|---|---|
| app | FastAPI приложение |
| postgres | Основная база данных |
| redis | Rate limit и временные данные |


## Миграции базы данных

При запуске контейнера выполняется команда:`alembic upgrade head` через скрипт `entrypoint.sh`.

# API


## Регистрация пользователя

### POST

```
/users/register
```


Пример запроса:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```


Ответ:

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2026-01-01T12:00:00"
}
```


---

## Авторизация


### POST

```
/users/login
```


Пример запроса:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```


Ответ:

```json
{
  "access_token": "jwt-token"
}
```


После получения токена необходимо передавать его в заголовке:

```
Authorization: Bearer <token>
```


---

## Получение пользователей


### GET

```
/users
```


Параметры пагинации:

| Параметр | Описание | По умолчанию |
|-|-|-|
| limit | количество записей | 50 |
| offset | смещение | 0 |


Пример:

```
GET /users?limit=10&offset=0
```


Ответ:

```json
[
  {
    "id": "uuid",
    "email": "user@example.com",
    "created_at": "2026-01-01T12:00:00"
  }
]
```


Endpoint требует авторизацию:

```
Authorization: Bearer <access_token>
```


# Rate Limit

Регистрация ограничена через Redis по IP-адресу клиента.

Текущая настройка:

```
5 запросов за 60 секунд
```

При превышении лимита API возвращает:

```http
429 Too Many Requests
```


# Переменные окружения


| Переменная | Назначение |
|-|-|
| APP_PORT | внешний порт приложения |
| POSTGRES_HOST | адрес PostgreSQL |
| POSTGRES_PORT | порт PostgreSQL |
| POSTGRES_DB | имя базы |
| POSTGRES_USER | пользователь БД |
| POSTGRES_PASSWORD | пароль БД |
| REDIS_HOST | адрес Redis |
| REDIS_PORT | порт Redis |
| JWT_SECRET_KEY | секрет JWT |
| JWT_ALGORITHM | алгоритм JWT |
| RATE_LIMIT_REQUESTS | количество запросов |
| RATE_LIMIT_WINDOW_SECONDS | окно ограничения |


## Локальный запуск без Docker

При запуске приложения напрямую через Python virtual environment необходимо заменить адреса сервисов:

```env
POSTGRES_HOST=localhost
REDIS_HOST=localhost
```