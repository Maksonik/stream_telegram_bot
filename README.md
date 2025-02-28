[![Test coverage](https://github.com/Maksonik/stream_telegram_bot/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Maksonik/stream_telegram_bot/actions/workflows/main.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ceecaeb449dfc82daaf8/test_coverage)](https://codeclimate.com/github/Maksonik/stream_telegram_bot/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/ceecaeb449dfc82daaf8/maintainability)](https://codeclimate.com/github/Maksonik/stream_telegram_bot/maintainability)

# Stream Telegram Bot

Stream Telegram Bot - это бот, который проверяет наличие запланированных трансляций на YouTube-канале и уведомляет о них в Telegram. После завершения трансляции бот автоматически удаляет соответствующие сообщения.

## 📌 Функциональность
- Проверяет YouTube-канал на наличие запланированных трансляций.
- Отправляет уведомление в Telegram-канал о предстоящем стриме.
- За 15 минут до начала стрима отправляет дополнительное уведомление.
- Удаляет сообщение о стриме после его завершения.

---
## 📌 Оповещения

Примеры оповещений, которые бот отправляет в Telegram, хранятся в файле **`scr/constants.py`**.

### Пример оповещений:

#### Оповещение о запланированном стриме:

- `"Запланирован стрим в {time}, не пропустите!\n{url}"`
- `"Стрим будет в {time}, присоединяйтесь.\n{url}"`

#### Оповещение за 15 минут до начала стрима:

- `"Стрим начнётся в {time}, осталось совсем немного!\n{url}"`
- `"До стрима в {time} осталось немного времени.\n{url}"`

## 🚀 Развертывание

### 1. 🔧 Установка зависимостей

Перед запуском убедитесь, что у вас установлен **Docker** и **Docker Compose**.

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/your-username/stream_telegram_bot.git
   cd stream_telegram_bot
   ```
2. Создайте `.env` файл, скопировав шаблон:
   ```bash
   cp env.template .env
   ```
3. Заполните `.env` файл нужными значениями:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token
   TELEGRAM_CHANNEL=your_telegram_channel_id
   YOUTUBE_CHANNEL_URL=your_youtube_channel_url
   REDIS_URL=redis://redis:6379/0
   ```

### 2. 🏗 Запуск бота

Запустить бота можно с помощью `make`:
```bash
make run
```
Или вручную через Docker Compose:
```bash
docker compose up --build
```

### 3. ⚡ Запуск Celery Worker и Beat

1. Запустить Celery Worker:
   ```bash
   make worker
   ```
2. Запустить Celery Beat (для периодических задач):
   ```bash
   make beat
   ```

Бот теперь будет проверять запланированные трансляции и отправлять уведомления в Telegram!

## 📜 Лицензия
Этот проект распространяется под лицензией MIT. Подробности в файле `LICENSE`.
