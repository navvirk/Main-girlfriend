import os
import telebot
import requests

# Get env vars
BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

if BOT_TOKEN is None or HF_TOKEN is None:
    raise ValueError("BOT_TOKEN or HF_TOKEN is not set! Check Railway or Replit variables.")

bot = telebot.TeleBot(BOT_TOKEN)

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi jaanu, tainu kivein yaad aaya? Likhi ja kuch...")

@bot.message_handler(func=lambda m: True)
def reply(message):
    try:
        prompt = f"Have a flirty, Punjabi girlfriend style chat. User said: {message.text}\nGF:"

        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 100,
                "temperature": 0.7
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code != 200:
            bot.reply_to(message, f"Oye hoye! HF error: {response.status_code} - {response.text}")
            return

        data = response.json()
        print("HF raw response:", data)

        if 'generated_text' in data[0]:
            answer = data[0]['generated_text'].split("GF:")[-1].strip()
        else:
            answer = "Sorry jaan, kujh galat ho gaya..."

        bot.reply_to(message, answer)

    except Exception as e:
        bot.reply_to(message, f"Oye hoye! Kujh error ho gaya sajna.\n{str(e)}")

print("Bot is running...")
bot.polling()
