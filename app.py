from asyncio import run
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import (router_start, router_user, router_password, router_admin, router_contact_admin)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    print('Ishga tushdi')
    dp.include_router(router_start)
    dp.include_router(router_admin)
    dp.include_router(router_user)
    dp.include_router(router_password)
    dp.include_router(router_contact_admin)
    await dp.start_polling(bot)

if __name__=='__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        print('Exit')