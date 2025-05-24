import os
import telebot
import requests

# Get tokens from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

def get_ai_reply(message):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    json_data = {"inputs": message}
    response = requests.post(
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
        headers=headers,
        json=json_data
    )
    try:
        generated = response.json()[0]["generated_text"]
        return generated
    except:
        return "Oye hoye! Kujh error ho gaya sajna."

@bot.message_handler(func=lambda msg: True)
def handle_all(msg):
    reply = get_ai_reply(msg.text)
    bot.send_message(msg.chat.id, reply)

print("Bot is running...")
bot.polling()
