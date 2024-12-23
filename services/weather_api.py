import requests
from config import TOKEN_WEATHER

API_KEY = TOKEN_WEATHER
BASE_URL = "http://dataservice.accuweather.com"

def get_weather(location: str, interval: str):
    try:
        # Получение ключа локации
        location_url = f"{BASE_URL}/locations/v1/cities/search"
        params = {"apikey": API_KEY, "q": location}
        response = requests.get(location_url, params=params)
        response.raise_for_status()
        location_key = response.json()[0]["Key"]

        # Получение прогноза
        forecast_url = f"{BASE_URL}/forecasts/v1/daily/{interval}day/{location_key}"
        response = requests.get(forecast_url, params={"apikey": API_KEY})
        response.raise_for_status()
        forecast = response.json()

        # Форматирование ответа
        result = ""
        for day in forecast["DailyForecasts"]:
            result += f"Дата: {day['Date']}\n" \
                      f"Температура: {day['Temperature']['Minimum']['Value']} - {day['Temperature']['Maximum']['Value']}°C\n" \
                      f"Описание: {day['Day']['IconPhrase']}\n\n"
        return result
    except Exception as e:
        return f"Ошибка получения прогноза: {e}"
