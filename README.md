# Telegram Mini App Clicker

Пример Telegram Mini App с фронтендом-кликером, Flask API и Telegram-ботом. Проект показывает передачу пользователя из бота в Web App и взаимодействие фронтенда с API.

## Возможности

- открытие Mini App из Telegram-бота;
- начисление монет за клики;
- хранение статистики пользователей в памяти процесса;
- таблица лидеров и обработка списания монет;
- команды бота для просмотра статистики.

## Стек

- HTML, CSS и JavaScript
- Telegram Web App API
- Python и Flask
- python-telegram-bot

## Быстрый старт

Создайте бота через BotFather, затем подготовьте окружение backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
```

Укажите `BOT_TOKEN` и HTTPS-адрес фронтенда в `backend/.env`. Запустите API:

```bash
python app.py
```

Telegram требует HTTPS для Web App и API. Опубликуйте фронтенд на HTTPS-хостинге и предоставьте API через HTTPS, затем задайте URL с параметром API:

```dotenv
FRONTEND_URL=https://example.com/?api=https://api.example.com/api
```

В отдельном процессе запустите бота:

```bash
cd backend
python bot.py
```

Демонстрационный фронтенд: `https://vernaculusf.github.io/Tg-miniapp-example/`.

## Структура проекта

```text
.
├── index.html          # разметка Mini App
├── style.css           # стили фронтенда
├── script.js           # логика кликера и запросы к API
├── backend/
│   ├── app.py          # Flask API
│   ├── bot.py          # Telegram-бот
│   └── requirements.txt
└── .env.example        # пример конфигурации
```

API хранит данные в памяти, поэтому состояние сбрасывается при перезапуске процесса.

## Лицензия

MIT
