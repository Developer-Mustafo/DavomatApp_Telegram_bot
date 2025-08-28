from aiogram import types, Router, F
from service import get_by_phone_number
router = Router()

@router.message(F.text == 'Parolni olish 🔐')
async def get_password(message:types.Message):
    phone_number = message.contact.phone_number
    password = get_by_phone_number(phone_number)
    await message.answer(f'Telefon raqam :{phone_number}'
                         f'Parol: {password}')