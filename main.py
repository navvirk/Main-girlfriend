import telebot
import requests

# Tokens
BOT_TOKEN = "7553740502:AAGTAu5Pla0MsLJ_pJ6XEgpjLrMUOvsWQZ8"
HF_TOKEN = "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"

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
        return "Sajna, thoda ruk ja, kuch error aa gaya!"

@bot.message_handler(func=lambda msg: True)
def handle_all(msg):
    reply = get_ai_reply(msg.text)
    bot.send_message(msg.chat.id, reply)

print("Bot is running...")
bot.polling()
