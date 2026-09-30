from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import db_manager


def get_cakes_keyboard():
    cakes_builder = ReplyKeyboardBuilder()
    cakes = db_manager.get_cakes()

    for cake in cakes:
        button_text = f"{cake['name']} - {cake['price']} руб."
        cakes_builder.add(KeyboardButton(text=button_text))

    cakes_builder.adjust(2)
    return cakes_builder.as_markup(resize_keyboard=True)