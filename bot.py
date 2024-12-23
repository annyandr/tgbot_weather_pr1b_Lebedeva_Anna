from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import TOKEN_BOT


bot = Bot(TOKEN_BOT)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Привет! Я помогу узнать прогноз погоды. Используй команду /help, чтобы узнать больше.")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply("/start - начать\n/help - помощь\n/weather - прогноз погоды")

if __name__ == "__main__":
    executor.start_polling(dp)