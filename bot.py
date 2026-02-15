import telebot
import google.generativeai as genai

# @BotFather ගෙන් ලැබුණු Token එක මෙතනට දාන්න
BOT_TOKEN = 'ඔයාගේ_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(BOT_TOKEN)

# User ගේ API Keys තාවකාලිකව තියාගන්න Dictionary එකක්
user_api_keys = {}

# /start command එක ලැබුණම
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = "ආයුබෝවන්! 👋\n\nකරුණාකර ඔයාගේ **Gemini API Key** එක මෙතනට එවන්න. 🔑"
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# මැසේජ් එකක් ආවම ක්‍රියාත්මක වන කොටස
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_text = message.text

    # තවම API Key එක දීලා නැත්නම්, එවපු මැසේජ් එක Key එකක් විදිහට සලකන්න
    if user_id not in user_api_keys:
        try:
            # API Key එක වැඩද බලන්න පොඩි test එකක් (Optional)
            genai.configure(api_key=user_text)
            model = genai.GenerativeModel('gemini-pro')
            user_api_keys[user_id] = user_text # Key එක save කරගන්නවා
            bot.reply_to(message, "සාර්ථකයි! ✅ ඔයාගේ Gemini API එක සම්බන්ධ වුණා. දැන් ඕනෑම ප්‍රශ්නයක් අහන්න.")
        except Exception as e:
            bot.reply_to(message, "වැරදි API Key එකක්. කරුණාකර නැවත උත්සාහ කරන්න.")
    
    # API Key එක දැනටමත් තියෙනවා නම්, Gemini හරහා උත්තර දෙන්න
    else:
        try:
            genai.configure(api_key=user_api_keys[user_id])
            model = genai.GenerativeModel('gemini-pro')
            
            # AI එකෙන් Response එක ගන්නවා
            response = model.generate_content(user_text)
            bot.reply_to(message, response.text)
            
        except Exception as e:
            bot.reply_to(message, "අයියෝ! Gemini එකෙන් උත්තරේ ගන්න බැරි වුණා. API Key එකේ ප්‍රශ්නයක් වෙන්න ඇති.")

print("බොට් වැඩ කරන්න පටන් ගත්තා...")
bot.polling()
