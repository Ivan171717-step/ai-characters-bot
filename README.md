# AI Characters Telegram Bot

Telegram-бот с AI-персонажами на базе OpenAI.

Пользователь выбирает персонажа и общается с ним в Telegram. Бот сохраняет историю диалога, чтобы ответы были более живыми и контекстными.

## Персонажи

- 👩 **Анастейша** — мягкое, поддерживающее и дружелюбное общение.
- 😏 **Джейсон** — сарказм, юмор, мемный стиль и лёгкие подколы.

## Возможности

- выбор AI-персонажа;
- ответы через OpenAI API;
- сохранение истории сообщений;
- SQLite-база данных;
- подготовка к деплою на Railway через `Procfile`;
- асинхронная архитектура на `aiogram`.

## Технологии

- Python 3.11+
- aiogram 3
- OpenAI API
- SQLAlchemy
- SQLite
- python-dotenv

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Ivan171717-step/ai-characters-bot.git
cd ai-characters-bot
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

Активировать окружение:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать `.env`

Скопируй пример переменных окружения:

```bash
cp .env.example .env
```

На Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Заполни `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

Где взять токены:

- `BOT_TOKEN` — создать бота через [@BotFather](https://t.me/BotFather)
- `OPENAI_API_KEY` — получить в аккаунте OpenAI

### 5. Запустить бота

```bash
python -m bot.main
```

После запуска открой своего Telegram-бота и отправь команду:

```text
/start
```

## Переменные окружения

| Переменная | Обязательная | Описание |
|---|---:|---|
| `BOT_TOKEN` | Да | Токен Telegram-бота от BotFather |
| `OPENAI_API_KEY` | Да | API-ключ OpenAI |

## Деплой на Railway

В проекте уже есть `Procfile`:

```Procfile
worker: python -m bot.main
```

Для деплоя на Railway:

1. Создай новый проект на Railway.
2. Подключи GitHub-репозиторий.
3. Добавь переменные окружения:
   - `BOT_TOKEN`
   - `OPENAI_API_KEY`
4. Запусти деплой.

## Структура проекта

```text
ai-characters-bot/
├── bot/
│   ├── main.py          # запуск бота и обработчики сообщений
│   ├── ai_service.py    # работа с OpenAI
│   ├── characters.py    # описание персонажей
│   ├── database.py      # подключение к базе данных
│   └── models.py        # SQLAlchemy-модели
├── .gitignore
├── Procfile
├── README.md
└── requirements.txt
```

## Важно

Не добавляй файл `.env` в GitHub. В нём находятся приватные токены.

## Планы по развитию

- добавить команды `/help`, `/reset`, `/character`;
- вынести настройки в `config.py`;
- добавить Dockerfile;
- улучшить структуру проекта;
- добавить PostgreSQL для production-деплоя;
- добавить лимиты бесплатного использования;
- добавить премиум-доступ.
