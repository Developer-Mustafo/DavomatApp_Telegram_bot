from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton
, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove)
# from aiogram.utils.keyboard import (
# ReplyKeyboardBuilder, InlineKeyboardBuilder
# )

clearButton = ReplyKeyboardRemove()

get_number = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Telefon raqamni berish 📱', request_contact=True)]
], one_time_keyboard=True, resize_keyboard=True)

user_option = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='To\'lov qilish 💳'), KeyboardButton(text='Parolni olish 🔐')]
], one_time_keyboard=True, resize_keyboard=True)

admin_option = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Foydalanuvchilar 👥'), KeyboardButton(text='Parolni olish 🔐')]
], one_time_keyboard=True, resize_keyboard=True)

to_my_channel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Mening kanalim', url='https://t.me/mustafo_rahim_android')]
])

admin_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Tasdiqlash', callback_data='approved'),
     InlineKeyboardButton(text='❌ Rad etish', callback_data='disapproved')]
])

#agar internetdan xabar chiqarmoqchi bo'lsang
# users = [
#     'Mustafo', '.', 'Zamira'
# ]
#
# async def inline_cars():
#     keyboard = ReplyKeyboardBuilder()
#     for user in users:
#         keyboard.add(KeyboardButton(text=user))
#     return keyboard.adjust(2).as_markup()