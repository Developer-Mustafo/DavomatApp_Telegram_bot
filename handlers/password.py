from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from model import phone_state
from service import get_by_phone_number
router = Router()
from config import ADMIN_ID
from keyboards import (user_option, admin_option, get_number)

@router.message(F.text == 'Parolni olish 🔐')
async def get_password(message:types.Message, state:FSMContext):
    await message.answer('Iltimos telefon raqamingizni bering 📱', reply_markup=get_number)
    await state.set_state(phone_state.wait)

@router.message(phone_state.wait, F.contact)
async def get_phone_number(message:types.Message, state:FSMContext):
    contact = message.contact
    phone_number = contact.phone_number
    person = get_by_phone_number(phone_number)
    option = None
    for admin_id in ADMIN_ID:
        if message.from_user.id == admin_id:
            option = admin_option
        else:
            option = user_option
    if person is None:
        await message.answer('Bunday foydalanuvchi yo\'q', reply_markup=option)
    else:
        password = person.password
        await message.answer(f'Telefon raqam : <code>{phone_number}</code>\nParol: <code>{password}</code>', parse_mode='HTML', reply_markup=option)
        await state.clear()