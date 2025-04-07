import telebot
from flask import Flask, request

API_TOKEN = '7833588361:AAGK31h7EFWLv0xHLvsbOlGtThIDwn-aDKw'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Webhook route
@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

# Basic route for test
@app.route('/')
def webhook():
    return 'Привет, это Андрей из виртуального мира!', 200

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Меня зовут Андрей. Я — психологический помощник из виртуального измерения. Чем могу помочь?')

# Простой ответ на любое сообщение
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f'Ты написал: "{message.text}". Я рядом.')

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://andrey-virtual-bot.onrender.com/' + API_TOKEN)
    app.run(host='0.0.0.0', port=10000)
