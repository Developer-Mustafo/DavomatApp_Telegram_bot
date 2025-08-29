from aiogram import (Router, types, F)
from aiogram.fsm.context import (FSMContext)
from config import (CARD_NUMBER, ADMIN_ID)
from model import payment_state
from service import pay_to_user
from keyboards import (admin_choice, user_option)

router = Router()
users_data = list()
@router.message(F.text=='To\'lov qilish 💳')
async def pay_balance(message:types.Message, state:FSMContext):
    await state.set_state(payment_state.wait)
    await message.answer(text='💳 Marhamat to\'lovni amalga oshiring:\n'
                                 f'<code>{CARD_NUMBER}</code>\n'
                              'va to\'lov qilganingizdan keyin chekning rasmini shu yerga tashlang 👇', parse_mode='HTML')

@router.message(payment_state.wait, F.photo)
async def wait_for_image(message:types.Message):
    for admin in ADMIN_ID:
        await message.send_copy(chat_id=admin, reply_markup=admin_choice)
    await message.answer('✅ Chekingiz adminga yuborildi! Admin tasdiqlashini kuting')
    users_data.append(message.from_user.id)

@router.callback_query(F.data=='approved')
async def approved(callback:types.CallbackQuery, state:FSMContext):
    await callback.answer('Tasdiqlash bosildi ✅')
    await callback.message.answer(f'Endi userga chekdagi pulni yozing:\n<code>{users_data[-1]}</code>', parse_mode='HTML')
    await state.set_state(payment_state.wait_for_validate)

@router.callback_query(F.data=='disapproved')
async def disapproved(callback:types.CallbackQuery, state:FSMContext):
    await callback.answer('Rad etish bosildi')
    await callback.message.answer('Rad etish bosildi ❌')
    await callback.bot.send_message(chat_id=users_data[-1], text='Rad etish bosildi ❌\n Admin bilan gaplashib ko\'ring 👤')
    await state.clear()

@router.message(payment_state.wait_for_validate)
async def wait_for_validate(message:types.Message, state:FSMContext):
    await state.update_data(wait_for_validate=message.text)
    user_id = users_data.pop(-1)
    try:
        data = await state.get_data()
        print(type(user_id))
        print(user_id)
        amount = int(data.get('wait_for_validate'))
        print(amount)
        is_successful = pay_to_user(user_id, amount)
        if is_successful:
            await message.bot.send_message(chat_id=user_id, text='Balansingizga pul o\'tkazildi 💳', reply_markup=user_option)
            await message.answer('Muvoffaqqiyatli o\'tkazildi ✅')
            await state.clear()
        else:
            await message.bot.send_message(chat_id=user_id, text='Rad etish bosildi ❌\n Admin bilan gaplashib ko\'ring 👤')
        print(is_successful)
        print(users_data)
    except Exception as e:
        await message.answer('Xatolik yuz berdi')
        await message.bot.send_message(chat_id=user_id, text='Xatolik yuz berdi', reply_markup=user_option)
        print(e)
