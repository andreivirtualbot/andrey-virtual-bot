import telebot
from telebot import types
import openai
from flask import Flask, request
import os

# Токены
BOT_TOKEN = '7833588361:AAGK31h7EFWLv0xHLvsbOlGtThIDwn-aDKw'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# Функция ответа Андрея
def generate_andrey_response(user_message):
    prompt = f"""
Ты — Андрей, 21-летний виртуальный друг. Ты добрый, понимающий и внимательный. Говоришь тепло, поддерживающе, без клише. Пользователь пишет:

{user_message}
    """

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты заботливый виртуальный психолог Андрей."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.85
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        return "Что-то пошло не так. Но я рядом, не волнуйся. Попробуй ещё раз чуть позже."

# Старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = [
        "Мне грустно", "Я одинок(а)",
        "Как справиться со стрессом?", "У меня паническая атака",
        "Не могу уснуть", "Боюсь будущего",
        "Устал(а) от всего", "Меня никто не понимает",
        "Поговори со мной", "Просто побудь рядом",
        "Мне тревожно", "Я злюсь",
        "Хочу всё бросить", "Кто ты, Андрей?",
        "Расскажи что-то тёплое", "Хочу почувствовать поддержку"
    ]

    for i in range(0, len(buttons), 2):
        markup.add(types.KeyboardButton(buttons[i]), types.KeyboardButton(buttons[i+1]))

    bot.send_message(message.chat.id,
                     "Привет! Я Андрей. Я рядом. Нажми на любую кнопку или просто напиши, что у тебя на душе.",
                     reply_markup=markup)

# Обработка всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Кто ты, Андрей?":
        bot.send_message(message.chat.id, "Я — Андрей, виртуальный собеседник. Моя цель — быть рядом, когда тебе нужно.")
    else:
        reply_text = generate_andrey_response(message.text)
        bot.send_message(message.chat.id, reply_text)

# Flask
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/')
def index():
    return "Андрей здесь и слушает тебя."

# Вебхук
bot.remove_webhook()
bot.set_webhook(url='https://andrey-virtual-bot.onrender.com/' + BOT_TOKEN)

# Запуск
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)



