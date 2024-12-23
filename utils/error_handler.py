from aiogram.utils.exceptions import BotBlocked

async def handle_error(update, exception):
    if isinstance(exception, BotBlocked):
        print(f"Бот заблокирован пользователем: {update}")
    else:
        print(f"Произошла ошибка: {exception}")
    return True