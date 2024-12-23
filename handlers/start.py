from aiogram.types import Message

async def cmd_start(message: Message):
    await message.answer("Привет! Я Weather Bot. Я помогу узнать прогноз погоды. Введите /help, чтобы узнать, как я работаю.")