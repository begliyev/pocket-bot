# python_version=3.10
# -*- coding: utf-8 -*-
import os
TG_TOKEN = "8596852225:AAeoLPcPgtbuaaibX5Z0qMWe0XoV0lOuUI4"
GEMINI_KEY = "AIzaSyCasEqUCSGDWOsULuoSCSjkLrZDFlqa5K4"
from aiohttp import web

# Koyeb'in beklediği sahte web sunucusu
async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get('/', handle)

if __name__ == '__main__':
    # Botu başlatırken aynı zamanda web sunucusunu da arka planda açar
    import asyncio
    loop = asyncio.get_event_loop()
    
    # Koyeb'in verdiği PORT değişkenini al, yoksa 8080 kullan
    port = int(os.environ.get("PORT", 8080))
    
    # Hem botu hem web sunucusunu çalıştır
    loop.create_task(dp.start_polling())
    web.run_app(app, port=port)
