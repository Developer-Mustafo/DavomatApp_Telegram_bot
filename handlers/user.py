from aiogram import (Router, types, F)
from config import (CARD_NUMBER)
router = Router()

@router.message(F.text=='To\'lov qilish 💳')
async def pay_balance(message:types.Message):
    await message.answer(text='💳 Marhamat to\'lovni amalga oshiring:\n'
                                 f'<code>{CARD_NUMBER}</code>\n'
                              'va to\'lov qilganingizdan keyin rasmni shu yerga tashlang 👇', parse_mode='HTML')