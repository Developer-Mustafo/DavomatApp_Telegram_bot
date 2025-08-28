from aiogram import types, Router
from aiogram.filters import CommandStart
from model import User
from config import ADMIN_ID
from keyboards import (get_number, to_my_channel, clearButton, user_option, admin_option)
from service import register_to_telegram

router = Router()
@router.message(CommandStart())
async def cmd_start(message:types.Message):
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    await message.answer(f'Assalomu aleykum {full_name} 👋', reply_markup=get_number)
    await message.answer('Xush kelibsiz !!!', reply_markup=to_my_channel)


@router.message(lambda message:message.contact)
async def contact_handler(message:types.Message):
    contact = message.contact
    user_id = contact.user_id
    first_name = contact.first_name or ''
    last_name = contact.last_name or ''
    phone_number = contact.phone_number or ''
    user = User(user_id, first_name, last_name, phone_number)
    await message.answer('Qabul qilindi', reply_markup=clearButton)
    for admin_id in ADMIN_ID:
        if user_id==admin_id:
            await message.answer('Xush kelibsiz admin', reply_markup=admin_option)
        else:
            await message.answer('Xush kelibsiz foydalanuvchi', reply_markup=user_option)
    print(user)
    register_to_telegram(user)
    #dbga saqlanadi
# @router.message(Command(commands='users'))
# async def cmd_users(message:types.Message):
#     await message.answer(text = 'mana hamma userlar',reply_markup=await inline_cars())
