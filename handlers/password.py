from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from model.passwordstate import PasswordState
from service import update_password
router = Router()
from config import ADMIN_ID
from keyboards import (user_option, admin_option, get_number)

@router.message(F.text == 'Parolni o\'zgartirish 🔐')
async def get_password(message:types.Message, state:FSMContext):
    await message.answer('Iltimos telefon raqamingizni bering 📱', reply_markup=get_number)
    await state.set_state(PasswordState.wait)

@router.message(PasswordState.wait, F.contact)
async def get_phone_number(message:types.Message, state:FSMContext):
    contact = message.contact
    phone_number = contact.phone_number
    await message.answer('Yangi parolni kiriting: ')
    await state.update_data(wait = phone_number)
    await state.set_state(PasswordState.password)

@router.message(PasswordState.password)
async def get_password(message:types.Message, state:FSMContext):
    data = await state.get_data()
    phone_number = data.get('wait')
    person = update_password(phone_number, message.text)
    print(person)
    await message.answer('Muvoffaqiyatli amalga oshirildi')
