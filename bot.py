import telebot
import google.generativeai as genai
import os
from flask import Flask
import threading

# --- සරල Web Server එක (Render එකට අවශ්‍යයි) ---
app = Flask(__name__)
@app.route('/')
def index():
    return "Bot is Running!"

def run_flask():
    # Render විසින් ලබාදෙන Port එක ලබා ගැනීම
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Telegram Bot කොටස ---
BOT_TOKEN = '8588448311:AAGCDpiVXZgTEn2tRpccQvUKzTEg7c1-J9Y' # මෙතනට ඔයාගේ Token එක දාන්න
bot = telebot.TeleBot(BOT_TOKEN)
user_api_keys = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ආයුබෝවන්! කරුණාකර ඔයාගේ Gemini API Key එක එවන්න. 🔑")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    if user_id not in user_api_keys:
        try:
            genai.configure(api_key=message.text)
            model = genai.GenerativeModel('gemini-pro')
            model.generate_content("test") # පොඩි ටෙස්ට් එකක්
            user_api_keys[user_id] = message.text
            bot.reply_to(message, "සාර්ථකයි! ✅ දැන් ප්‍රශ්නයක් අහන්න.")
        except:
            bot.reply_to(message, "වැරදි API Key එකක්. නැවත එවන්න.")
    else:
        try:
            genai.configure(api_key=user_api_keys[user_id])
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(message.text)
            bot.reply_to(message, response.text)
        except:
            bot.reply_to(message, "Error එකක් ආවා. සමහරවිට API Key එකේ අවුලක්.")

# --- ප්‍රධාන ක්‍රියාදාමය ---
if __name__ == "__main__":
    # Flask server එක වෙනම thread එකක run කරනවා
    threading.Thread(target=run_flask).start()
    
    print("Bot is polling...")
    bot.infinity_polling()
