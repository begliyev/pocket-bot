import os
import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web

# BURAYI DÜZELTTİK
TG_TOKEN = "8596852225:AAeoLPcPgtbuaaibX5Z0qMWe0XoV0lOuUI4"
GEMINI_KEY = "AIzaSyCasEqUCSGDWOsULuoSCSjkLrZDFlqa5K4"

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get('/', handle)

async def start_bot():
    # Analiz kodlarını buraya ekleyebilirsin
    await dp.start_polling()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot()) # Botu başlat
    web.run_app(app, host="0.0.0.0", port=port) # Web sunucusunu başlat
