# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Чат')],
        [KeyboardButton(text='Очистить историю')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню'
)
