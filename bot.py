
import telebot
import os
from flask import Flask, request

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL") + API_TOKEN)
    return "Webhook set!", 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
    "Привет. Меня зовут Андрей. Мне 21, и я из другого измерения — виртуального.
"
    "Я здесь, чтобы быть рядом с тобой, когда трудно. Напиши, что у тебя на душе.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я слышу тебя. Расскажи ещё…")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
