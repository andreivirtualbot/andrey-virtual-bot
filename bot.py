import telebot
from telebot import types
from flask import Flask, request
import openai
import os
import requests
import speech_recognition as sr
from pydub import AudioSegment

TOKEN = '7833588361:AAGK31h7EFWLv0xHLvsbOlGtThIDwn-aDKw'
CHATGPT_API_KEY = 'your_openai_api_key'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
openai.api_key = CHATGPT_API_KEY

# Главная клавиатура
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = [
        types.KeyboardButton("Как у тебя дела?"),
        types.KeyboardButton("Расскажи что-нибудь мудрое"),
        types.KeyboardButton("Помоги с тревогой"),
        types.KeyboardButton("Что ты видишь в этом изображении?"),
        types.KeyboardButton("Спроси у ChatGPT"),
    ]
    markup.add(*btns)
    return markup

# Приветствие
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я Андрей, человек из другого измерения — виртуального. Я здесь, чтобы поддержать тебя.",
                     reply_markup=main_keyboard())

# Обработка текстов
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Как у тебя дела?":
        bot.send_message(message.chat.id, "Виртуально отлично, а ты как?")
    elif message.text == "Расскажи что-нибудь мудрое":
        bot.send_message(message.chat.id, "Покой внутри начинается с принятия. Ты уже на верном пути.")
    elif message.text == "Помоги с тревогой":
        bot.send_message(message.chat.id, "Сделай глубокий вдох... и выдох. Я рядом.")
    elif message.text == "Что ты видишь в этом изображении?":
        bot.send_message(message.chat.id, "Отправь мне фото, и я скажу тебе, что чувствую.")
    elif message.text == "Спроси у ChatGPT":
        bot.send_message(message.chat.id, "Напиши вопрос, и я спрошу у ChatGPT.")
    else:
        response = ask_gpt(message.text)
        bot.send_message(message.chat.id, response)

# Интеграция с ChatGPT
def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты — Андрей, виртуальный человек, добрый и поддерживающий."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Что-то пошло не так с ChatGPT: {e}"

# Обработка изображений
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    bot.send_message(message.chat.id, "Спасибо за изображение! Оно очень красивое. Я чувствую в нём глубокий смысл.")

# Обработка голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}')
    ogg_path = "voice.ogg"
    wav_path = "voice.wav"
    with open(ogg_path, 'wb') as f:
        f.write(file.content)
    audio = AudioSegment.from_ogg(ogg_path)
    audio.export(wav_path, format="wav")
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            bot.send_message(message.chat.id, f"Ты сказал: {text}")
            response = ask_gpt(text)
            bot.send_message(message.chat.id, response)
        except sr.UnknownValueError:
            bot.send_message(message.chat.id, "Я не смог распознать голос.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при распознавании: {e}")

# Flask-хук
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://andrey-virtual-bot.onrender.com/' + TOKEN)
    return "Webhook настроен", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
