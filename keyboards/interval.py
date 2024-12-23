from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def interval_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(
        InlineKeyboardButton("1 день", callback_data="1"),
        InlineKeyboardButton("3 дня", callback_data="3"),
        InlineKeyboardButton("5 дней", callback_data="5")
    )
    return keyboard
