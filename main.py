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

        if response.status_code != 200:
            bot.reply_to(message, f"Oye hoye! AI error: {response.status_code} - {response.text}")
            return

        result = response.json()
        reply = result[0]["generated_text"]
        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, f"Oye hoye! Python error: {str(e)}")

bot.polling()
