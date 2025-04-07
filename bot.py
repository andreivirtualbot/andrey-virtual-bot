import telebot
import openai
import os
from flask import Flask, request
from telebot import types

# Получение токенов из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# Главное меню с кнопками
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Поговори со мной", "Поддержи меня")
    markup.row("Расскажи анекдот", "Дай совет")
    markup.row("Как стать лучше?", "Что почитать?")
    markup.row("Погода", "Мотивация", "Расслабиться")
    return markup

# Ответ на старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я Андрей — твой виртуальный друг и помощник. Чем могу помочь?",
        reply_markup=main_menu()
    )

# Обработка текста и запрос к ChatGPT
@bot.message_handler(func=lambda m: True)
def chat_with_gpt(message):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — виртуальный друг Андрей. Ты отзывчивый, тёплый, немного шутливый и очень поддерживающий."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, reply, reply_markup=main_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

# Webhook
@app.route("/" + TELEGRAM_TOKEN, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Бот Андрей работает!", 200

# Установка webhook
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_TOKEN}")
    app.run(host="0.0.0.0", port=10000)
