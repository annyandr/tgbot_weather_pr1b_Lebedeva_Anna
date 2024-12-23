from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from services.weather_api import get_weather_forecast
from keyboards.interval import interval_keyboard

# Обновляем состояния
class WeatherForm(StatesGroup):
    start_point = State()
    end_point = State()
    intermediate_stops = State()
    interval = State()

# Обработчик команды /weather
async def cmd_weather(message: types.Message):
    """Запускает процесс получения прогноза погоды и маршрута."""
    await message.reply("Введите начальную точку маршрута (город или населенный пункт, на английском языке):")
    await WeatherForm.start_point.set()

# Обработчик ввода начальной точки маршрута
async def process_start_point(message: types.Message, state: FSMContext):
    """Обрабатывает ввод начальной точки маршрута."""
    start_point = message.text
    await state.update_data(start_point=start_point)
    await message.reply("Введите конечную точку маршрута (город или населенный пункт, на английском языке):")
    await WeatherForm.end_point.set()

# Обработчик ввода конечной точки маршрута
async def process_end_point(message: types.Message, state: FSMContext):
    """Обрабатывает ввод конечной точки маршрута."""
    end_point = message.text
    await state.update_data(end_point=end_point)
    await message.reply("Введите промежуточные остановки (если есть, разделяя запятыми, город или населенный пункт, на английском языке):")
    await WeatherForm.intermediate_stops.set()

# Обработчик ввода промежуточных остановок
async def process_intermediate_stops(message: types.Message, state: FSMContext):
    """Обрабатывает ввод промежуточных остановок маршрута."""
    intermediate_stops = message.text
    await state.update_data(intermediate_stops=intermediate_stops)
    
    # Запрос интервала прогноза
    await message.reply("Выберите временной интервал прогноза:", reply_markup=interval_keyboard())
    await WeatherForm.interval.set()

# Обработчик выбора временного интервала
async def process_interval(callback_query: types.CallbackQuery, state: FSMContext):
    """Обрабатывает выбор временного интервала."""
    interval = callback_query.data
    user_data = await state.get_data()

    start_point = user_data["start_point"]
    end_point = user_data["end_point"]
    intermediate_stops = user_data["intermediate_stops"]

    # Формируем список точек маршрута
    points = [start_point, end_point] + [stop.strip() for stop in intermediate_stops.split(",")] if intermediate_stops else []

    # Собираем прогнозы для каждой точки маршрута
    forecasts = ""
    for point in points:
        forecast = get_weather_forecast(point, interval)
        forecasts += f"Прогноз погоды для {point}:\n{forecast}\n\n"

    route_info = (
        f"Маршрут: {start_point} -> {end_point}\n"
        f"Промежуточные остановки: {intermediate_stops if intermediate_stops else 'Нет'}\n"
        f"Интервал прогноза: {interval} дней\n"
    )

    if forecasts:
        await callback_query.message.reply(route_info + forecasts)
    else:
        await callback_query.message.reply("Не удалось получить прогноз погоды. Попробуйте снова.")
    
    await state.finish()

# Регистрация хендлеров
from aiogram.dispatcher import Dispatcher

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_weather, commands=["weather"])
    dp.register_message_handler(process_start_point, state=WeatherForm.start_point)
    dp.register_message_handler(process_end_point, state=WeatherForm.end_point)
    dp.register_message_handler(process_intermediate_stops, state=WeatherForm.intermediate_stops)
    dp.register_callback_query_handler(process_interval, state=WeatherForm.interval)
