import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import requests
from config import TELEGRAM_TOKEN, OPENWEATHER_API_KEY

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = f"🌤 Погода в {data['name']}:\nТемпература: {data['main']['temp']}°C\nОщущается как: {data['main']['feels_like']}°C\nВлажность: {data['main']['humidity']}%\nСостояние: {data['weather'][0]['description'].capitalize()}"
        return weather
    else:
        return "Город не найден или ошибка API."

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я WeatherBot 🌦\nОтправь мне название города, чтобы узнать погоду.")

def weather(update: Update, context: CallbackContext):
    city = update.message.text
    weather_info = get_weather(city)
    update.message.reply_text(weather_info)

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, weather))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
