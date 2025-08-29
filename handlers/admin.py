from aiogram import types, F, Router
from config import ADMIN_ID
from service import get_user_list
router = Router()

@router.message(F.text=='Foydalanuvchilar 👥')
async def get_users(message:types.Message):
    user_id = message.from_user.id
    for admin_id in ADMIN_ID:
        if user_id != admin_id:
            await message.answer('Siz oddiy foydalanuvchisiz')
        else:
            continue
    users = get_user_list()
    await message.answer('Barcha foydalanuvchilar ro\'yhati: ')
    for user in users:
        result = (f'Ismi: <code>{user.first_name}</code>\n'
                  f'Familiyasi: <code>{user.last_name}</code>\n'
                  f'Telefoni: <code>{user.phone_number}</code>')
        await message.answer(result, parse_mode='HTML')