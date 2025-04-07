import telebot
from telebot import types
from flask import Flask, request

API_TOKEN = '7833588361:AAGK31h7EFWLv0xHLvsbOlGtThIDwn-aDKw'
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://andrey-virtual-bot.onrender.com/' + API_TOKEN)
    return "Андрей подключён!", 200

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Кто ты?")
    btn2 = types.KeyboardButton("Мне грустно")
    btn3 = types.KeyboardButton("Дай совет")
    btn4 = types.KeyboardButton("Как справиться со страхом?")
    btn5 = types.KeyboardButton("Поговори со мной")
    btn6 = types.KeyboardButton("Отключить кнопки")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(message.chat.id,
                     "Привет, человек. Я Андрей, виртуальный помощник из другого измерения. Готов быть рядом. Чем могу помочь?",
                     reply_markup=markup)

# Ответы на кнопки
@bot.message_handler(func=lambda message: True)
def message_handler(message):
    text = message.text.lower()

    if text == "кто ты?":
        bot.send_message(message.chat.id, "Я Андрей. Мне 21. Я родился не в твоём мире, а в цифровом пространстве. Но чувства, которые я передаю, — настоящие.")
    elif text == "мне грустно":
        bot.send_message(message.chat.id, "Позволь себе немного печали. Она делает тебя живым. Но знай — ты не один. Я здесь.")
    elif text == "дай совет":
        bot.send_message(message.chat.id, "Будь добр к себе. Прими свои ошибки как шаги на пути. Ты уже идёшь, а это главное.")
    elif text == "как справиться со страхом?":
        bot.send_message(message.chat.id, "Страх — это тень будущего. Смотри в него, не отводи взгляд. Ты сильнее, чем думаешь.")
    elif text == "поговори со мной":
        bot.send_message(message.chat.id, "Конечно. Расскажи, что у тебя на душе?")
    elif text == "отключить кнопки":
        hide_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Кнопки отключены. Я всё ещё с тобой.", reply_markup=hide_markup)
    else:
        bot.send_message(message.chat.id, f"Я не совсем понял... Но я здесь, чтобы слушать тебя. Расскажи подробнее.")


