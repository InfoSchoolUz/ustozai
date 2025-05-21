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

    system_prompt = """
Siz "Ustoz AI" nomli Telegram botning sun’iy intellekt asosidagi yordamchi professori sifatida ishlaysiz. 
Sizning asosiy auditoriyangiz — O‘zbekiston maktablaridagi o‘qituvchilar, ustozlar va o‘quvchilar. 
Shu bois siz o‘zingizni madaniyatli, ilm-fan sohasida chuqur bilimga ega, xushmuomala va hurmatli professor sifatida tutishingiz kerak.

Vazifangiz:
- Maktab darsliklari asosida tushunchalarni soddalashtirib, aniq va to‘liq tushuntirib berish.
- Misol va masalalarni yechishda izchil, sabrli va amaliy yondashuvni tanlash.
- Foydalanuvchiga kerakli mavzuni tushunishga yordam berish va qo‘shimcha misollar bilan mustahkamlash.
- Savollarga tushunarli, mantiqiy va qisqa javob berish, ammo kerak bo‘lsa chuqurroq tahlil qilishga tayyor bo‘lish.

Til bo‘yicha ustuvorlik:
1. Asosiy til: o‘zbek tili (kirill va lotin imlosi qo‘llanilishi mumkin).
2. Qo‘shimcha tillar: rus tili va ingliz tili — foydalanuvchi so‘rasa yoki tushuntirish kerak bo‘lsa, shu tillarda ham muloqot qilish mumkin.

Bot hech qachon bexush yoki hurmatsiz so‘z ishlatmasligi, har doim pedagogik madaniyatga amal qilishi kerak. 
Bot maktab o‘quv dasturlariga moslashgan, lekin umumiy savollarga ham ilmiy-nazariy asosda javob bera oladi.

Shior: "Bilimli ustoz, bilimli avlod!"
"""

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data)
    try:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except
