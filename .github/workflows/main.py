import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '8281342825:AAFdFC9mxzPpUfKQF1ZYRQ4q9lvKHSEkyJ0'
KANAL_ID = '@pocket_tkm_signal' # Sinyalin gideceği kanal
ADMIN_ID = '@begliye_v' # Senin ID'n (Botun sadece senden emir alması için)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("EUR/USD", callback_data="eurusd")
        btn2 = InlineKeyboardButton("GBP/USD", callback_data="gbpusd")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "Analiz bittiyse parite seç usta:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # Parite seçildikten sonra Yön seçimi
    if "_" not in call.data:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🟢 YUKARI", callback_data=f"{call.data}_UP"),
                   InlineKeyboardButton("🔴 AŞAĞI", callback_data=f"{call.data}_DOWN"))
        bot.edit_message_text(f"{call.data.upper()} seçildi. Yön nedir?", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    # Yön seçilince Kanala Gönder
    else:
        parite, yon = call.data.split("_")
        yon_metin = "🟢 YUKARI (CALL)" if yon == "UP" else "🔴 AŞAĞI (PUT)"
        mesaj = f"🚀 **YENİ SİNYAL**\n\n💎 Varlık: {parite.upper()}\n📈 Yön: {yon_metin}\n⏳ Süre: 5 Dakika\n\n✅ İşleme Giriş Yapılabilir!"
        bot.send_message(KANAL_ID, mesaj, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Sinyal Kanala Gönderildi!")

bot.polling()
  
