import telebot
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        user_input = message.text
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"inputs": user_input}

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            reply = data[0]['generated_text']
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, f"HF Error {response.status_code}:\n{response.text}")

    except Exception as e:
        bot.reply_to(message, f"Bot crashed:\n{str(e)}")

bot.polling()
