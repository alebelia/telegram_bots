# Отображает курсы доллара США, евро и фунта стерлингов к рублю на сегодня (по данным ЦБ)

import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import xml.etree.ElementTree as ET
import datetime
from Env_params import currency_tkn # Импорт токена от BotFather

# Вкл. логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Необходимые параметры
url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='

def get_current_date():
    """Получить текущую дату в заданном формате"""
    current_date = datetime.datetime.now()
    return current_date.strftime('%d/%m/%Y')

def get_currency_dict(url):
    """Получить данные о курсах доллара США, евро и фунта стерлингов к рублю"""
    full_url = url + get_current_date()
    data = requests.get(full_url)
    root = ET.fromstring(data.content)
    data_dict = {}
    for child in root:
        currency_name = child[1].text
        currency_value = child[4].text
        data_dict[currency_name] = currency_value
    return data_dict['USD'], data_dict['EUR'], data_dict['GBP']


def show_currency(update: Update, context: CallbackContext):
    """Вывести курсы доллара США, евро и фунта стерлингов к рублю на сегодня"""
    update.message.reply_text('Курс доллара США на сегодня: ' + str(get_currency_dict(url)[0]) + '\nКурс евро: ' + str(get_currency_dict(url)[1]) + '\nКурс фунта стерлингов: '+ str(get_currency_dict(url)[2]))

def start(update: Update, context: CallbackContext):
    """Отображение приветствия при вводе команды /start"""
    update.message.reply_text('Привет! Введи /currency, чтобы увидеть сегодняшние курсы доллара США, евро и фунта стерлингов к рублю.')

def main():
    updater = Updater(currency_tkn)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("currency", show_currency))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()