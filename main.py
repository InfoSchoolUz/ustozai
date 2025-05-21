import telebot
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    name = message.from_user.first_name
    text = f"Assalomu alaykum, {name}! Men ustozlarga yordam beradigan botman. Menga savolingizni yuboring."
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        javob = get_ai_response(message.text)
        bot.send_message(message.chat.id, javob)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik: {e}")

def get_ai_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "Sen ustozlarga yordam beradigan intellektual yordamchisan."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data)
    try:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"AI xatosi: {e}"

# Bot ishga tushirilmoqda
print("Bot ishga tushmoqda...")
time.sleep(2)
bot.remove_webhook()
bot.infinity_polling()
