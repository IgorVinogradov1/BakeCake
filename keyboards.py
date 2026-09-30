from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_cakes_keyboard():
    cakes_builder = ReplyKeyboardBuilder()
    cakes_builder.add(
        KeyboardButton(text="Свадебный 'Нежность'"),
        KeyboardButton(text="Популярный 'Юбилей'"),
        KeyboardButton(text="Шоколадный 'Брауни'"),
        KeyboardButton(text="Ягодный 'Восторг'"),
        KeyboardButton(text="Детский 'Карамелька'"),
        KeyboardButton(text="Праздничный 'Бархат'")
    )
    cakes_builder.adjust(2)
    return cakes_builder.as_markup(resize_keyboard=True)