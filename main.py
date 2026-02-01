import telebot
import os
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1. WEB SUNUCUSU AYARI (Render Hatasını Çözmek İçin)
app = Flask('')

@app.route('/')
def home():
    return "Bot Aktif!"

def run():
    # Render'ın beklediği portu açıyoruz
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. BOT AYARLARI
TOKEN = 'BOT_TOKEN_BURAYA'
ADMIN_ID = 12345678  # Senin ID'n
KANAL_ID = '@kanal_adiniz'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'panel'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        markup = InlineKeyboardMarkup()
        pariteler = ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY", "BTC/USD"]
        for p in pariteler:
            markup.add(InlineKeyboardButton(p, callback_data=p))
        bot.send_message(message.chat.id, "📊 Analiz hazırsa parite seç:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if "_" not in call.data:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("🟢 YUKARI", callback_data=f"{call.data}_UP"),
            InlineKeyboardButton("🔴 AŞAĞI", callback_data=f"{call.data}_DOWN")
        )
        bot.edit_message_text(f"🎯 {call.data} için yön nedir?", call.message.chat.id, call.message.message_id, reply_markup=markup)
    else:
        parite, yon = call.data.split("_")
        yon_yazi = "YUKARI (CALL)" if yon == "UP" else "AŞAĞI (PUT)"
        emoji = "🚀" if yon == "UP" else "📉"
        mesaj = f"{emoji} **POCKET SİNYAL** {emoji}\n\n💎 **Varlık:** {parite}\n↕️ **Yön:** {yon_yazi}\n⏱ **Vade:** 1-5 Dakika"
        bot.send_message(KANAL_ID, mesaj, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Gönderildi!")

# 3. ÇALIŞTIRMA (Aynı anda hem web sitesini hem botu başlatır)
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot ve Web Sunucusu çalışıyor...")
    bot.infinity_polling()
