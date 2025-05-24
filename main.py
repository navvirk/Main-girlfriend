import os
import telebot
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = "microsoft/DialoGPT-medium"  # You can change this to any text-generation model
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

bot = telebot.TeleBot(BOT_TOKEN)

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

        # Always print full response
        bot.reply_to(message, f"STATUS: {response.status_code}\nTEXT: {response.text}")

    except Exception as e:
        bot.reply_to(message, f"ERROR: {str(e)}")
