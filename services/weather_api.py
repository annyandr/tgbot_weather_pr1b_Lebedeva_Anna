import requests
from config import TOKEN_WEATHER

BASE_URL = "http://dataservice.accuweather.com"

def get_city_location(city_name: str):
    """Получает ключ местоположения для города."""
    url = f"{BASE_URL}/locations/v1/cities/search"
    params = {"apikey": TOKEN_WEATHER, "q": city_name}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]["Key"]  # Ключ местоположения
        else:
            return None
    except (requests.RequestException, KeyError) as e:
        print(f"Ошибка получения местоположения: {e}")
        return None

def get_weather_forecast(city_name: str) -> str:
    """Получает прогноз погоды для указанного города."""
    location_key = get_city_location(city_name)
    if not location_key:
        return "Город не найден. Проверьте правильность написания."

    url = f"{BASE_URL}/forecasts/v1/daily/1day/{location_key}"
    params = {"apikey": TOKEN_WEATHER, "language": "ru", "metric": True}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Извлечение данных из ответа API
        forecast = data["DailyForecasts"][0]
        date = forecast["Date"]
        temperature = forecast["Temperature"]
        min_temp = temperature["Minimum"]["Value"]
        max_temp = temperature["Maximum"]["Value"]
        weather_text = forecast["Day"]["IconPhrase"]

        return (
            f"Прогноз на {date[:10]}:\n"
            f"Минимальная температура: {min_temp}°C\n"
            f"Максимальная температура: {max_temp}°C\n"
            f"Погодные условия: {weather_text}"
        )
    except (requests.RequestException, KeyError) as e:
        print(f"Ошибка получения прогноза погоды: {e}")
        return "Не удалось получить прогноз погоды. Попробуйте позже."
