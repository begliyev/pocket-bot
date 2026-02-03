import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import yfinance as yf
import pandas_ta as ta
import google.generativeai as genai

# TOKEN BİLGİLERİ (Tırnak içindekileri BotFather ve Google'dan aldıklarınla değiştir)
TG_TOKEN = "8596852225:AAeoLPcPgtbuaaibX5Z0qMWe0XoV0lOuUI4"
GEMINI_KEY = "AIzaSyCasEqUCSGDWOsULuoSCSjkLrZDFlqa5K4"

# Yapay Zeka Kurulumu
genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

async def get_trading_analysis(symbol):
    try:
        df = yf.download(symbol, period='1d', interval='15m')
        df['RSI'] = ta.rsi(df['Close'], length=14)
        last_price = round(df['Close'].iloc[-1], 5)
        last_rsi = round(df['RSI'].iloc[-1], 2)
        
        prompt = f"{symbol} paritesinde fiyat={last_price} ve RSI={last_rsi}. Pocket Option için 1 dakikalık yön tahmini yap."
        response = ai_model.generate_content(prompt)
        return f"📊 **Sembol:** {symbol}\n💰 **Fiyat:** {last_price}\n📉 **RSI:** {last_rsi}\n\n🤖 **AI Analizi:**\n{response.text}"
    except Exception as e:
        return f"Hata oluştu: {e}"

@dp.message_handler(commands=['analiz'])
async def start_analysis(message: types.Message):
    await message.answer("🔄 Analiz ediliyor...")
    result = await get_trading_analysis("EURUSD=X")
    await message.answer(result, parse_mode="Markdown")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
