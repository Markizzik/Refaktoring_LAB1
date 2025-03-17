import requests
from telebot import *
token='8139819279:AAGbDbUaN8xwuWRe2qKLnfw-sPQ9a_1FoG0'
# token='6569790433:AAHf4EqiHhASTokEn1YTDKwKaLb3LYakM84'
city = "Moscow,RU"
lat = "37.674874"
lon = "55.636135"
appid = "3c211ea758fa910484bf5ccc4d69b593"
bot=telebot.TeleBot(token)
markup = None

def res_data():
    global data
    res = requests.get('http://api.openweathermap.org/data/2.5/weather',
                       params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
def cityget(gor):
    global city
    if gor == "msk":
        city = "Moscow,RU"
    elif gor == 'spb':
        city = 'Saint Petersburg,RU'
    elif gor == 'msk_zam':
        city = 'Zamoskvorechye,RU'
    elif gor == 'msk_sv':
        city = 'Sviblovo,RU'

@bot.message_handler(commands=['start'])
def hello(message):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # buttton1=types.KeyboardButton('/pogoda_day')
    # buttton3 = types.KeyboardButton('/best_tgc')
    # markup.add(buttton2,buttton1,buttton3)
    print(message)
    bot.send_message(message.chat.id,'\
Привет!\n   Это бот mopi, который может отображать актуальную погоду в мире \n\
    Введите /button для удобного управления ботом с помощью кнопок')
    # bot.send_message(message.chat.id, 'выберите что вам надо')
@bot.message_handler(commands=['button'])
def button(message):
    markup = types.InlineKeyboardMarkup()
    buttton1=types.InlineKeyboardButton('Погода на день' , callback_data='day')
    but3 = types.InlineKeyboardButton('Быстрые варианты городов', callback_data='gor')
    but4 = types.InlineKeyboardButton('Убрать кнопки',callback_data='del')
    but5 = types.InlineKeyboardButton('Помощь', callback_data='help')
    markup.add(buttton1)
    markup.add(but3)
    markup.add(but4)
    markup.add(but5)
    bot.send_message(message.chat.id,'Меню:',reply_markup=markup)
@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == 'day':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        # print(callback.message)
        pogoda_day(callback.message)
        button(callback.message)
    elif callback.data == 'gor':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        markup = types.InlineKeyboardMarkup()
        buttton1 = types.InlineKeyboardButton('Санкт-Петербург', callback_data='spb')
        but3 = types.InlineKeyboardButton('Москва', callback_data='msk')
        markup.row( buttton1, but3)
        bot.send_message(callback.message.chat.id, 'Выберите город:', reply_markup=markup)
    elif callback.data == 'msk':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        cityget('msk')
        button(callback.message)
    elif callback.data == 'spb':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        cityget('spb')
        button(callback.message)
    elif callback.data == 'del':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
    elif callback.data == 'help':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        help(callback.message)
        markup = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton('Назад', callback_data='be')
        markup.row(but1)
        bot.send_message(callback.message.chat.id,'Вернуться в меню',reply_markup=markup)
    elif callback.data == 'be':
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id)
        bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.id - 1)
        button(callback.message)
@bot.message_handler(commands=['help'])
def help(message):
    print(message)
    bot.send_message(message.chat.id,'\
/start - Вывод приветствия \n\
/pogoda_day - Погода на день \n\
Установить город - city <город>,<страна (например RU-Росссия)> ( <> - знаки разделения, их писать не нужно ), городом по умолчанию является Москва\n\
Пример: city Mosсow,RU \n\
/button - Вывод меню \n\
/help - Вывод данной подсказки\n\
')

@bot.message_handler(commands=['pogoda_day'])
def pogoda_day(message):
    bot.send_message(message.chat.id, 'Погода на день:')
    res_data()
    global data
    mes = (
            "Город: < " + str(city) + ' >\n' + "Погодные условия: < " + str(data['weather'][0]['description']) + ' >\n' +
              "Температура: < " + str(data['main']['temp']) + ' >\n' + "Минимальная температура: < " + str(data['main']['temp_min']) + ' >\n'
              + "Максимальная температура: < " + str(data['main']['temp_max']) + ' >\n' + 'Скорость ветра: < ' + str(data['wind']['speed'])+ ' >'
           )
    print(message)
    bot.send_message(message.chat.id,mes)

@bot.message_handler(content_types=['text'])
def answer(message):
    global city
    if message.text.lower()[:4:]=='city':
        city=str(message.text)[5::]
        bot.send_message(message.chat.id,'Готово! Установлен ваш город \nГород: '+ city)
    elif message.text.lower()=='мтуси':
        bot.send_message(message.chat.id , 'https://mtuci.ru')
    elif message.text.lower()== 'msk':
        cityget('msk')
        bot.send_message(message.chat.id, 'Готово')
    elif message.text.lower()== 'spb':
        cityget('spb')
        bot.send_message(message.chat.id, 'Готово')
    elif message.text.lower()== 'msk_zam':
        cityget('msk_zam')
        bot.send_message(message.chat.id, 'Готово')
    elif message.text.lower()== 'msk_sv':
        cityget('msk_sv')
        bot.send_message(message.chat.id, 'Готово')
    else:
        bot.send_message(message.chat.id, 'Команда не распознанна')


@bot.message_handler(content_types=['location'])
def locat(message):
    print(message.location)
    global lat,lon
    lat = message.location.latitude
    lon = message.location.longitude

    res = requests.get('http://api.openweathermap.org/data/2.5/weather',
                       params={'lon': lon, 'lat': lat, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    mes = (
            "Погода в этом месте:" + '\n' + "Погодные условия:<" + str(data['weather'][0]['description']) + '>\n' +
            "Температура:<" + str(data['main']['temp']) + '>\n' + "Минимальная температура:<" + str(
        data['main']['temp_min']) + '>\n'
            + "Максимальная температура:<" + str(data['main']['temp_max']) + '>\n' + 'Скорость ветра:<' + str(
        data['wind']['speed']) + '>'
    )
    bot.send_message(message.chat.id, mes)
    print(lat,lon)
bot.polling()