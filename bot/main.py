import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

# Включаем логирование, чтобы видеть в консоли, что происходит с ботом
logging.basicConfig(level=logging.INFO)


async def main():
    # Инициализируем бота и диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Здесь чуть позже мы зарегистрируем наши обработчики (handlers)

    print("Бот успешно запущен и готов к работе!")

    # Запускаем бота в режиме ожидания сообщений
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
