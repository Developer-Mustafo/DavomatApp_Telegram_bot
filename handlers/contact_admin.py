import datetime
import io
import json
from dataclasses import asdict
from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from keyboards import (stop_conversation, admin_choice_for_conversation, admin_option, user_option)
from model import (Conversation, contact_admin_state)

router = Router()
chat_user = []
conversations = []

@router.message(F.text=='Admin bilan bo\'g\'lanish 👤')
async def contact_admin(message:types.Message, state:FSMContext):
    chat_user.clear()
    chat_user.append(message.from_user.id)
    await message.answer('👤 Siz suhbatni boshladingiz', reply_markup=stop_conversation)
    for admin_id in ADMIN_ID:
        await message.bot.send_message(chat_id=admin_id, text=f'👤 Foydalanuvchi {message.from_user.id} chatni boshladi. Qabul qilasizmi ?',
                                       reply_markup=admin_choice_for_conversation)
    await state.set_state(contact_admin_state.start)

@router.callback_query(F.data=='start')
async def start_conversation(callback:types.CallbackQuery, state:FSMContext):
    await callback.answer(text='Siz suxbatni boshladingiz ✅')
    await callback.message.answer('Siz suxbatni boshladingiz ✅', reply_markup=stop_conversation)
    for admin_id in ADMIN_ID:
        if admin_id not in chat_user:
            chat_user.append(admin_id)
    await state.set_state(contact_admin_state.start)

@router.callback_query(F.data=='cancel')
async def cancel_conversation(callback:types.CallbackQuery):
    await callback.answer(text='Siz suxbatni bekor qildingiz ❌')
    await callback.message.answer('Siz suxbatni bekor qildingiz ❌')
    user_id = chat_user[-1]
    await callback.bot.send_message(chat_id=user_id, text='Iltimos birozdan so\'ng urinib ko\'ring 🕛')
    chat_user.remove(user_id)

@router.message(F.text, F.text!='Chatni to\'xtatish ❌', contact_admin_state.start)
async def conversation(message:types.Message):
    sender_id = message.from_user.id
    if sender_id in chat_user:
        if sender_id in ADMIN_ID:
            for user_id in chat_user:
                if user_id not in ADMIN_ID:
                    await message.bot.send_message(chat_id=user_id, text=message.text)
        else:
            for admin_id in ADMIN_ID:
                if admin_id in chat_user:
                    await message.copy_to(chat_id=admin_id)
        conversations.append(Conversation(sender_id, message.text))
        for c in conversations:
            print(c)
    else:return

@router.message(F.text=='Chatni to\'xtatish ❌', contact_admin_state.start)
async def stop(message:types.Message, state:FSMContext):
    sender_id = message.from_user.id
    if sender_id in chat_user:
        for user_id in chat_user:
            if user_id in ADMIN_ID:
                await message.bot.send_message(chat_id=user_id, text='Chat to\'xtatildi', reply_markup=admin_option)
            else:
                await message.bot.send_message(chat_id=user_id, text='Chat to\'xtatildi', reply_markup=user_option)
    await state.clear()
    chat_user.clear()
    #listni json qilish/class @dataclass bo'lishi shart
    json_data = json.dumps([asdict(c) for c in conversations], indent=4)
    file_buffer = io.BytesIO(json_data.encode("utf-8"))
    file_buffer.name = "people.txt"  # Telegram uchun nom berish kerak
    file_name = f'conversation_{datetime.datetime.now()}.txt'
    document = types.BufferedInputFile(file_buffer.getvalue(), filename=file_name)
    # Faylni adminga yuborish
    for admin_id in ADMIN_ID:
        await message.bot.send_document(chat_id=admin_id, document=document)