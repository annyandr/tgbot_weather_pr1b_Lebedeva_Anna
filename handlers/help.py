from aiogram.types import Message

async def cmd_help(message: Message):
    await message.answer("Доступные команды:\n"
                         "/start - Начать работу с ботом\n"
                         "/help - Информация о командах\n"
                         "/weather - Узнать прогноз погоды")
