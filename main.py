import os
import telebot
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

if BOT_TOKEN is None or HF_TOKEN is None:
    raise ValueError("BOT_TOKEN or HF_TOKEN is not set!")

bot = telebot.TeleBot(BOT_TOKEN)

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi jaanu, likh na kuch hor gallan karan layi.")

@bot.message_handler(func=lambda m: True)
def reply(message):
    try:
        payload = {"inputs": message.text}
        response = requests.post(API_URL, headers=headers, json=payload)

        print("HF raw response:", response.text)

        data = response.json()

        if isinstance(data, list) and 'generated_text' in data[0]:
            reply_text = data[0]['generated_text']
        elif 'generated_text' in data:
            reply_text = data['generated_text']
        elif 'error' in data:
            reply_text = f"HF Error: {data['error']}"
        else:
            reply_text = "Jaanu, kujh galti ho gayi."

        bot.reply_to(message, reply_text)

    except Exception as e:
        print("Error:", str(e))
        bot.reply_to(message, f"Oye hoye! Kujh error ho gaya sajna.\n{str(e)}")

print("Bot is running...")
bot.polling()
