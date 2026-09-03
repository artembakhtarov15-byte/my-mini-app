# Телеграм-бот с общением в стиле Яндекс.Алисы

Этот бот использует YandexGPT для имитации общения в стиле Яндекс.Алисы.

## Требования

- Python 3.8+
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
- Yandex Cloud аккаунт с доступом к YandexGPT

## Установка

1. Клонируйте репозиторий или создайте папку проекта

2. Создайте виртуальное окружение и установите зависимости:
```bash
python3 -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Настройте переменные окружения:
   - Скопируйте `.env.example` в `.env`
   - Заполните файл `.env` своими данными:
     - `TELEGRAM_BOT_TOKEN` — токен вашего Telegram-бота
     - `YANDEX_IAM_TOKEN` — IAM-токен Yandex Cloud
     - `YANDEX_FOLDER_ID` — ID каталога Yandex Cloud

## Как получить токены Yandex Cloud

### 1. IAM-токен (временный, действует 1 час)
```bash
yc iam-token create
```

### 2. Folder ID
```bash
yc config get folder-id
```

Или найдите в консоли Yandex Cloud: https://console.cloud.yandex.ru

## Запуск бота

```bash
python bot.py
```

## Использование

1. Отправьте команду `/start` боту в Telegram
2. Напишите любое сообщение
3. Бот ответит в стиле Яндекс.Алисы, используя YandexGPT

## Структура проекта

- `bot.py` — основной код бота
- `.env` — файл с настройками (не коммитить в git!)
- `.env.example` — пример файла настроек
- `requirements.txt` — список зависимостей

## Примечания

- IAM-токен действует 1 час. Для долгой работы нужно обновлять его или использовать сервисный аккаунт
- Бот хранит session_id для каждого пользователя в памяти (сбрасывается при перезапуске)
- Для продакшена рекомендуется использовать базу данных для хранения сессий
