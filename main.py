import os
import telebot
import requests

# Read environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

if BOT_TOKEN is None or HF_TOKEN is None:
    raise ValueError("BOT_TOKEN or HF_TOKEN is not set! Check Railway/Replit secrets.")

bot = telebot.TeleBot(BOT_TOKEN)

# Headers for Hugging Face API
headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Working chatbot model (replace if needed)
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
TRANSLATE_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-pa"

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi jaanu, tainu kivein yaad aaya? Likhi ja kuch...")

# Main reply handler
@bot.message_handler(func=lambda m: True)
def reply(message):
    try:
        user_input = message.text

        # Step 1: Generate English response using chatbot
        payload = {"inputs": user_input}
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            bot.reply_to(message, f"Oye hoye! HF error: {response.status_code} - {response.reason}")
            return
        
        data = response.json()
        print("HF chatbot response:", data)

        if 'generated_text' in data:
            english_reply = data['generated_text']
        elif isinstance(data, list) and 'generated_text' in data[0]:
            english_reply = data[0]['generated_text']
        else:
            bot.reply_to(message, "Sorry jaan, kujh samajh nahi aaya...")
            return

        # Step 2: Translate English response to Punjabi
        translation_payload = {"inputs": english_reply}
        translation_response = requests.post(TRANSLATE_URL, headers=headers, json=translation_payload)
        
        if translation_response.status_code != 200:
            bot.reply_to(message, f"Oye hoye! Translation error: {translation_response.status_code} - {translation_response.reason}")
            return

        translated_data = translation_response.json()
        print("HF translation response:", translated_data)

        if isinstance(translated_data, list) and 'translation_text' in translated_data[0]:
            punjabi_reply = translated_data[0]['translation_text']
        else:
            punjabi_reply = "Oye hoye! Kujh translate nahi ho paya."

        # Send translated message
        bot.reply_to(message, punjabi_reply)

    except Exception as e:
        bot.reply_to(message, f"Oye hoye! Kujh error ho gaya sajna.\n{str(e)}")

# Start polling
print("Bot is running...")
bot.polling()
