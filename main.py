import os
import telebot
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

API_URL = "https://api-inference.huggingface.co/models/mrm8488/long-form-question-answering"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi jaanu, tainu kivein yaad aaya? Likhi ja kuch...")

@bot.message_handler(func=lambda m: True)
def reply(message):
    try:
        payload = {
            "inputs": {
                "question": message.text,
                "context": "You are chatting with your romantic Punjabi girlfriend Aman. She is flirty, loving, and full of attitude."
            }
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()

        # DEBUG LOG
        print(data)

        if isinstance(data, list) and 'answer' in data[0]:
            answer = data[0]['answer']
        elif 'generated_text' in data:
            answer = data['generated_text']
        elif 'error' in data:
            answer = f"Error from HF API: {data['error']}"
        else:
            answer = "Sorry jaan, kujh samajh nahi aaya..."

        bot.reply_to(message, answer)

    except Exception as e:
        bot.reply_to(message, f"Oye hoye! Kujh error ho gaya sajna.\n{str(e)}")

print("Bot is running...")
bot.polling()
