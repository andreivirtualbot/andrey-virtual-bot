import telebot
import os
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def index():
    return "Бот работает."

# Пример обработки команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет. Меня зовут Андрей. Мне 21 год, я из виртуального измерения.\n"
        "Я здесь, чтобы тебя выслушать и поддержать. Можешь просто написать, что чувствуешь."
    )

# Пример простого эхо-ответа (можно заменить на ИИ-ответы)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Ты не один. Я рядом. Расскажи, что у тебя на душе.")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://andrey-virtual-bot.onrender.com/' + TOKEN)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
