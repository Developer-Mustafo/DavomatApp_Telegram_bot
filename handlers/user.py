from aiogram import (Router, types, F)
from aiogram.fsm.context import (FSMContext)
from config import (CARD_NUMBER, ADMIN_ID)
from model import ImageState
from service import pay_to_user
from keyboards import (admin_choice)

router = Router()
users_need_to_pay = list()
@router.message(F.text=='To\'lov qilish 💳')
async def pay_balance(message:types.Message, state:FSMContext):
    await state.set_state(ImageState.wait)
    await message.answer(text='💳 Marhamat to\'lovni amalga oshiring:\n'
                                 f'<code>{CARD_NUMBER}</code>\n'
                              'va to\'lov qilganingizdan keyin chekning rasmini shu yerga tashlang 👇', parse_mode='HTML')

@router.message(ImageState.wait, F.photo)
async def wait_for_image(message:types.Message):
    for admin in ADMIN_ID:
        await message.send_copy(chat_id=admin, reply_markup=admin_choice)
    users_need_to_pay.append(message.from_user.id)
    await message.answer('Kutib turing xabaringiz yuborildi...')

@router.callback_query(F.data=='approved')
async def approved(callback:types.CallbackQuery, state:FSMContext):
    await callback.answer('Tasdiqlash bosildi ✅')
    await callback.message.answer(f'Endi userga chekdagi pulni yozing:\n<code>{users_need_to_pay[-1]}</code>', parse_mode='HTML')
    await state.set_state(ImageState.wait_for_validate)

@router.callback_query(F.data=='disapproved')
async def disapproved(callback:types.CallbackQuery, state:FSMContext):
    await callback.answer('Rad etish bosildi')
    await callback.message.answer('Rad etish bosildi ❌')
    await callback.bot.send_message(chat_id=users_need_to_pay[-1], text='Rad etish bosildi ❌\n Admin bilan gaplashib ko\'ring 👤')
    await state.clear()

@router.message(ImageState.wait_for_validate)
async def wait_for_validate(message:types.Message, state:FSMContext):
    await state.update_data(wait_for_validate=message.text)
    try:
        data = await state.get_data()
        for user_id in users_need_to_pay:
            print(type(user_id))
            print(user_id)
            amount = int(data.get('wait_for_validate'))
            print(amount)
            pay_to_user(user_id, amount)
            await message.bot.send_message(chat_id=user_id, text='Balansingizga pul o\'tkazildi 💳')
        await state.clear()
    except Exception:
        await message.answer('Xatolik yuz berdi')