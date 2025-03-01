[![Test coverage](https://github.com/Maksonik/stream_telegram_bot/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Maksonik/stream_telegram_bot/actions/workflows/main.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ceecaeb449dfc82daaf8/test_coverage)](https://codeclimate.com/github/Maksonik/stream_telegram_bot/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/ceecaeb449dfc82daaf8/maintainability)](https://codeclimate.com/github/Maksonik/stream_telegram_bot/maintainability)

# Stream Telegram Bot

Stream Telegram Bot is a bot that checks for scheduled YouTube streams and sends notifications about them in Telegram. After the stream ends, the bot automatically deletes the corresponding messages.

## 📌 Functionality
- Checks a YouTube channel for scheduled streams.
- Sends a notification to a Telegram channel about an upcoming stream.
- Sends an additional notification 15 minutes before the stream starts.
- Deletes the stream message after it ends.

## 📌 Notifications
Examples of notifications the bot sends to Telegram are stored in the `scr/constants.py` file.

### Example Notifications:

#### Scheduled stream notification (russian):
- `"Запланирован стрим в {time}, не пропустите!\n{url}"`
- `"Стрим будет в {time}, присоединяйтесь.\n{url}"`

#### 15 minutes before the stream starts (russian):
- `"Стрим начнётся в {time}, осталось совсем немного!\n{url}"`
- `"До стрима в {time} осталось немного времени.\n{url}"`

## 🚀 Deployment

### 1. 🔧 Installing dependencies
Before starting, make sure you have **Docker** and **Docker Compose** installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/stream_telegram_bot.git
   cd stream_telegram_bot
   ```

2. Create a `.env` file by copying the template:
   ```bash
   cp env.template .env
   ```

3. Fill in the `.env` file with the required values:
   ```env
   # TELEGRAM
   TELEGRAM_TOKEN=TOKEN
   TELEGRAM_CHANNEL=@the_forever_student
   
   # YOUTUBE
   YOUTUBE_CHANNEL_URL=https://www.youtube.com/@the_forever_student_live
   
   # REDIS
   REDIS_URL=redis://localhost:6379
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

### 2. 🏗 Running the bot
You can run the bot using `make`:

```bash
make run
```

Or manually through Docker Compose:

```bash
docker compose up --build
```

### 3. ⚡ Running Celery Worker and Beat
1. Run Celery Worker:
   ```bash
   make worker
   ```

2. Run Celery Beat (for periodic tasks):
   ```bash
   make beat
   ```

The bot will now check scheduled streams and send notifications to Telegram!

## 📜 License
This project is licensed under the MIT license. Details can be found in the `LICENSE` file.

---

# Stream Telegram Bot

Stream Telegram Bot - это бот, который проверяет наличие запланированных трансляций на YouTube-канале и уведомляет о них в Telegram. После завершения трансляции бот автоматически удаляет соответствующие сообщения.

## 📌 Функциональность
- Проверяет YouTube-канал на наличие запланированных трансляций.
- Отправляет уведомление в Telegram-канал о предстоящем стриме.
- За 15 минут до начала стрима отправляет дополнительное уведомление.
- Удаляет сообщение о стриме после его завершения.


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
   # TELEGRAM
   TELEGRAM_TOKEN=TOKEN
   TELEGRAM_CHANNEL=@the_forever_student
   
   # YOUTUBE
   YOUTUBE_CHANNEL_URL=https://www.youtube.com/@the_forever_student_live
   
   # REDIS
   REDIS_URL=redis://localhost:6379
   REDIS_HOST=localhost
   REDIS_PORT=6379
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
