from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from services.weather_api import get_weather_forecast

# Определяем состояния
class WeatherForm(StatesGroup):
    city = State()

# Обработчик команды /weather
async def cmd_weather(message: types.Message):
    """Запускает процесс получения прогноза погоды."""
    await message.reply("Введите название города для получения прогноза погоды:")
    await WeatherForm.city.set()  # Устанавливаем состояние

# Обработчик ввода города
async def process_city(message: types.Message, state: FSMContext):
    """Обрабатывает ввод города и выводит прогноз погоды."""
    city = message.text
    forecast = get_weather_forecast(city)
    
    if forecast:
        await message.reply(forecast)
    else:
        await message.reply("Извините, не удалось получить данные. Попробуйте снова.")
    
    await state.finish()  # Завершаем состояние

# Регистрация хендлеров
from aiogram.dispatcher import Dispatcher

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_weather, commands=["weather"])
    dp.register_message_handler(process_city, state=WeatherForm.city)
