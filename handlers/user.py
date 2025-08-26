from aiogram import (Router, types, F)
from aiogram.fsm.context import (FSMContext)
from config import (CARD_NUMBER, ADMIN_ID)
from model import ImageState
router = Router()

@router.message(F.text=='To\'lov qilish 💳')
async def pay_balance(message:types.Message, state:FSMContext):
    await state.set_state(ImageState.wait)
    await message.answer(text='💳 Marhamat to\'lovni amalga oshiring:\n'
                                 f'<code>{CARD_NUMBER}</code>\n'
                              'va to\'lov qilganingizdan keyin rasmni shu yerga tashlang 👇', parse_mode='HTML')

@router.message(ImageState.wait, F.photo)
async def wait_for_image(message:types.Message, state:FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await photo.bot.get_file(file_id=file_id)
    file_path = file.file_path
    image = await photo.bot.download_file(file_path)

    print(photo)
    for admin in ADMIN_ID:
        await message.send_copy(chat_id=admin)
    await state.clear()