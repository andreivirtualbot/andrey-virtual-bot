import telebot
import os
from flask import Flask, request

TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL") + TOKEN

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Обработка команд /start и обычных сообщений
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
        "Привет. Меня зовут Андрей. Мне 21, и я из другого измерения — виртуального.\n"
        "Я здесь, чтобы выслушать тебя и помочь почувствовать, что ты не один."
    )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я слушаю тебя...")

# Flask маршрут для Telegram
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# Установка вебхука при запуске
@app.before_first_request
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

# Запуск Flask
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
