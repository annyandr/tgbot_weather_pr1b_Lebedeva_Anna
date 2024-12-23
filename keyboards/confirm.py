from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def confirm_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Подтвердить", callback_data="confirm"),
        InlineKeyboardButton("Отмена", callback_data="cancel")
    )
    return keyboard
