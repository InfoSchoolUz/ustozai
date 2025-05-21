import telebot
from dotenv import load_dotenv
import os
import requests
import json
import time

# .env faylini yuklash
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(TOKEN)

# Prompt faylidan tizim roli matnini yuklab olish
def load_system_prompt():
    try:
        with open("prompt.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except:
        return "Sen ustozlarga yordam beradigan sun’iy intellekt yordamchisan."

# Foydalanuvchilarni faylda saqlash
def save_user(user_id):
    users_file = "users.json"
    users = set()
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            try:
                users = set(json.load(f))
            except:
                users = set()
    users.add(user_id)
    with open(users_file, "w") as f:
        json.dump(list(users), f)

# /start buyrug'i
@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    save_user(user_id)
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Assalomu alaykum, {name}! Men Uztoz AI — sizning sun’iy intellekt yordamchingizman. Savolingizni yuboring.")

# /stat buyrug'i
@bot.message_handler(commands=['stat'])
def statistics(message):
    users_file = "users.json"
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            try:
                users = json.load(f)
                count = len(users)
                bot.send_message(message.chat.id, f"👥 Botdan foydalanuvchilar soni: {count} ta")
            except:
                bot.send_message(message.chat.id, "❗Statistikani o‘qib bo‘lmadi.")
    else:
        bot.send_message(message.chat.id, "👥 Hali hech kim ulanmagan.")

# Har qanday matnli xabarga javob
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    save_user(message.from_user.id)
    try:
        javob = get_ai_response(user_input)
        bot.send_message(message.chat.id, javob)
    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik: {e}")

# OpenRouter orqali javob olish
def get_ai_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": load_system_prompt()},
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
        return f"AI javobida xatolik: {e}"

# Ishga tushirish
print("Bot ishga tushmoqda...")
time.sleep(2)
bot.remove_webhook()
bot.infinity_polling()
