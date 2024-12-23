from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.interval import interval_keyboard
from keyboards.confirm import confirm_keyboard
from services.weather_api import get_weather

class WeatherState(StatesGroup):
    location = State()
    interval = State()
    confirmation = State()

async def cmd_weather(message: Message):
    await message.answer("Введите город, чтобы узнать погоду:")
    await WeatherState.location.set()

async def process_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer("Выберите временной интервал:", reply_markup=interval_keyboard())
    await WeatherState.next()

async def process_interval(callback: CallbackQuery, state: FSMContext):
    await state.update_data(interval=callback.data)
    data = await state.get_data()
    await callback.message.answer(f"Вы запросили прогноз для {data['location']} на {data['interval']} дней. Подтвердите:", 
                                   reply_markup=confirm_keyboard())
    await WeatherState.next()

async def confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    weather_data = get_weather(data['location'], data['interval'])
    await callback.message.answer(weather_data)
    await state.finish()
