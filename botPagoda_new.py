import requests
import telebot
from telebot import types

TOKEN = ''
APPID = '3c211ea758fa910484bf5ccc4d69b593'
bot = telebot.TeleBot(TOKEN)

CITIES = {
    'msk': 'Moscow,RU',
    'spb': 'Saint Petersburg,RU',
    'msk_zam': 'Zamoskvorechye,RU',
    'msk_sv': 'Sviblovo,RU'
}

def get_weather_data(city):
    """Получить данные погоды для города."""
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather',
        params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': APPID}
    )
    return response.json()

def format_weather_message(data, city):
    """Форматирование сообщения с данными погоды."""
    return (
        f"Город: <{city}>\n"
        f"Погодные условия: <{data['weather'][0]['description']}>\n"
        f"Температура: <{data['main']['temp']}°C>\n"
        f"Минимальная температура: <{data['main']['temp_min']}°C>\n"
        f"Максимальная температура: <{data['main']['temp_max']}°C>\n"
        f"Скорость ветра: <{data['wind']['speed']} м/с>"
    )

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(
        message.chat.id,
        'Привет! Это бот mopi, который может отображать актуальную погоду в мире. '
        'Введите /button для удобного управления ботом с помощью кнопок.'
    )

@bot.message_handler(commands=['button'])
def button(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('Погода на день', callback_data='day'),
        types.InlineKeyboardButton('Быстрые варианты городов', callback_data='gor'),
        types.InlineKeyboardButton('Убрать кнопки', callback_data='del'),
        types.InlineKeyboardButton('Помощь', callback_data='help')
    )
    bot.send_message(message.chat.id, 'Меню:', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'day':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        display_weather(callback.message)
        button(callback.message)
    elif callback.data == 'gor':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        display_city_selection(callback.message)
    elif callback.data in CITIES:
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        display_weather_for_city(callback.message, callback.data)
    elif callback.data == 'del':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    elif callback.data == 'help':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        help_message(callback.message)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, (
        '/start - Вывод приветствия\n'
        '/pogoda_day - Погода на день\n'
        'Установить город: city <город>,<страна> (например RU)\n'
        '/button - Вывод меню\n'
        '/help - Вывод подсказки'
    ))

@bot.message_handler(commands=['pogoda_day'])
def display_weather(message):
    city = CITIES.get('msk', 'Moscow,RU')  # По умолчанию Москва
    weather_data = get_weather_data(city)
    weather_message = format_weather_message(weather_data, city)
    bot.send_message(message.chat.id, weather_message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.lower()
    if text.startswith('city'):
        city_name = text[5:].strip()
        # Set city dynamically or validate here
        bot.send_message(message.chat.id, f'Готово! Установлен ваш город: {city_name}')
    elif text in CITIES:
        city = CITIES.get(text, 'Moscow,RU')
        bot.send_message(message.chat.id, f'Готово! Город установлен: {city}')
    else:
        bot.send_message(message.chat.id, 'Команда не распознана')

@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat, lon = message.location.latitude, message.location.longitude
    weather_data = requests.get(
        'http://api.openweathermap.org/data/2.5/weather',
        params={'lat': lat, 'lon': lon, 'units': 'metric', 'lang': 'ru', 'APPID': APPID}
    ).json()
    weather_message = format_weather_message(weather_data, f"Latitude: {lat}, Longitude: {lon}")
    bot.send_message(message.chat.id, weather_message)

def display_city_selection(message):
    markup = types.InlineKeyboardMarkup()
    for key, city in CITIES.items():
        markup.add(types.InlineKeyboardButton(city.split(',')[0], callback_data=key))
    bot.send_message(message.chat.id, 'Выберите город:', reply_markup=markup)

def display_weather_for_city(message, city_key):
    city = CITIES.get(city_key, 'Moscow,RU')
    weather_data = get_weather_data(city)
    weather_message = format_weather_message(weather_data, city)
    bot.send_message(message.chat.id, weather_message)
    button(message)

bot.polling()
