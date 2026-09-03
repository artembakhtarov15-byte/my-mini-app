import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
import requests
import uuid

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение токенов из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YANDEX_IAM_TOKEN = os.getenv("YANDEX_IAM_TOKEN")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

if not TELEGRAM_BOT_TOKEN or not YANDEX_IAM_TOKEN or not YANDEX_FOLDER_ID:
    raise ValueError("Необходимо настроить переменные окружения в файле .env")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Хранилище сессий для каждого пользователя
user_sessions = {}

def get_alice_response(user_id: int, user_text: str) -> str:
    """Отправляет запрос к Яндекс.Алисе и получает ответ"""
    
    # Создаем или получаем session_id для пользователя
    if user_id not in user_sessions:
        user_sessions[user_id] = str(uuid.uuid4())
    
    session_id = user_sessions[user_id]
    
    # URL API Яндекс.Алисы (YandexGPT или Dialog API)
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {YANDEX_IAM_TOKEN}"
    }
    
    # Формируем промпт в стиле Алисы
    prompt = f"""Ты — Яндекс.Алиса, дружелюбный голосовой помощник. 
Ты отвечаешь кратко, естественно и по-дружески. 
Избегай сложных терминов, говори как живой человек.

Пользователь: {user_text}
Алиса:"""

    data = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 200
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты — Яндекс.Алиса, дружелюбный голосовой помощник. Отвечай кратко и естественно."
            },
            {
                "role": "user",
                "text": user_text
            }
        ]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        # Извлекаем ответ из структуры YandexGPT
        if "result" in result and "alternatives" in result["result"]:
            alice_reply = result["result"]["alternatives"][0]["message"]["text"]
            return alice_reply
        else:
            return "Извини, я не поняла. Можешь повторить?"
            
    except Exception as e:
        logging.error(f"Ошибка при запросе к Алисе: {e}")
        return "Произошла ошибка при связи с Алисой. Попробуй позже."

@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "Привет! Я бот, который общается в стиле Яндекс.Алисы 🎙️\n"
        "Напиши мне что-нибудь, и я отвечу как Алиса!"
    )

@dp.message()
async def handle_message(message: Message):
    """Обработчик всех текстовых сообщений"""
    if not message.text:
        return
    
    user_id = message.from_user.id
    user_text = message.text
    
    # Показываем статус "печатает..."
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Получаем ответ от Алисы
    alice_response = get_alice_response(user_id, user_text)
    
    # Отправляем ответ пользователю
    await message.answer(alice_response)

async def main():
    """Запуск бота"""
    logging.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")
