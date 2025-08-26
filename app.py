from asyncio import run
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router_start, router_admin
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    print('Ishga tushdi')
    dp.include_router(router_start)
    dp.include_router(router_admin)
    await dp.start_polling(bot)

if __name__=='__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        print('Exit')