from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import TOKEN_BOT
from handlers import start, help, weather

# Инициализация бота и диспетчера
bot = Bot(TOKEN_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация хендлеров
dp.register_message_handler(start.cmd_start, commands=["start"])
dp.register_message_handler(help.cmd_help, commands=["help"])
weather.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp)
