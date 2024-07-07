# user.py
from aiogram import Router, F
from aiogram.types import Message as TgMessage
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.generators import gpt_text
from app.states import Chat
from app.database.requests import set_user, add_message, get_chat_history, clear_chat_history
from config import SYSTEM_PROMPT, AI_MODEL, DEFAULT_TEMPERATURE, MAX_TOKENS

user = Router()

@user.message(CommandStart())
async def cmd_start(message: TgMessage):
    await set_user(message.from_user.id)
    await message.answer('Добро пожаловать', reply_markup=kb.main)

@user.message(F.text == 'Чат')
async def chatting(message: TgMessage, state: FSMContext):
    await state.set_state(Chat.active)
    await message.answer('Введите ваш запрос')

@user.message(F.text == 'Очистить историю')
async def clear_history_button(message: TgMessage):
    if await clear_chat_history(message.from_user.id):
        await message.answer("История чата очищена.", reply_markup=kb.main)
    else:
        await message.answer("Не удалось очистить историю чата.", reply_markup=kb.main)

@user.message(Chat.active)
async def chat_response(message: TgMessage, state: FSMContext):
    user_id = message.from_user.id
    
    # Получаем историю чата
    chat_history = await get_chat_history(user_id)
    
    # Добавляем текущее сообщение пользователя
    await add_message(user_id, message.text, 'user')
    
    # Формируем контекст для модели
    context = [{"role": "system", "content": SYSTEM_PROMPT}]
    context.extend([{"role": role, "content": content} for role, content in chat_history])
    context.append({"role": "user", "content": message.text})
    
    # Получаем ответ от модели
    # response = await gpt_text(context, AI_MODEL)
    
    response = await gpt_text(
        context, 
        AI_MODEL, 
        temperature=DEFAULT_TEMPERATURE, 
        max_tokens=MAX_TOKENS
    )

    # Сохраняем ответ модели
    await add_message(user_id, response, 'assistant')
    
    await message.answer(response)