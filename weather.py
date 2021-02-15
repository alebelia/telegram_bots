# Отображает текущую погоду в Москве

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
from Env_params import weather_tkn, weather_api_key # Импорт токена от BotFather и API key с openweathermap.org

# Вкл. логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Необходимые параметры
city_id = '524901' # ID Москвы на openweathermap.org
url = 'http://api.openweathermap.org/data/2.5/weather?id=' + city_id + '&appid=' + weather_api_key + '&lang=ru' + '&units=metric'


def start(update: Update, context: CallbackContext):
    """Отображение приветствия при вводе команды /start"""
    update.message.reply_text('Привет! Введи /weather, чтобы узнать, какая сейчас погода в Москве!')

def get_weather(city_id, url):
    """Получить данные о погоде"""
    contents = requests.get(url).json()
    city_name = contents['name']
    weather_desc = contents['weather'][0]['description']
    temp_min = contents['main']['temp_min']
    temp_max = contents['main']['temp_max']
    feels_like = contents['main']['feels_like']
    humidity = contents['main']['humidity']
    forecast = 'Город: ' + city_name + '\nПогода: ' + weather_desc + '\nМин. температура: ' + str(temp_min) + '\nМакс. температура: ' + str(temp_max) + '\nОщущается как: ' + str(feels_like) + '\nВлажность: ' + str(humidity) + '%'
    return forecast

def weather_forecast(update: Update, context: CallbackContext):
    """Вывести данные о погоде"""
    update.message.reply_text(get_weather(city_id, url))

def main():
    updater = Updater(weather_tkn)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", weather_forecast))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()