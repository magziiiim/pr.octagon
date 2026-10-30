import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

from database.base import SessionLocal
from database.crud import get_or_create_user, save_message

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # При старте тоже можем сохранить пользователя в БД
    db = SessionLocal()
    try:
        get_or_create_user(
            db, 
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
    finally:
        db.close()
        
    await message.answer("Бот-сборщик корпоративных переписок запущен! Я начал слушать чат.")

# Обработчик всех текстовых сообщений для сбора переписки
@dp.message()
async def collect_messages(message: types.Message):
    # Игнорируем сообщения без текста (пока берем только текст, позже расширим на файлы/фото)
    if not message.text:
        return

    db = SessionLocal()
    try:
        # 1. Сохраняем или получаем пользователя
        user = get_or_create_user(
            db,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )

        # 2. Сохраняем сообщение в базу данных
        save_message(
            db,
            telegram_message_id=message.message_id,
            user_id=user.telegram_id,
            chat_id=message.chat.id,
            text=message.text
        )
        
        logging.info(f"Сохранено сообщение от {message.from_user.username}: {message.text}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении сообщения в БД: {e}")
    finally:
        db.close()

async def main():
    logging.info("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен.")