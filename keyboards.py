from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import db_manager


def get_phone_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Поделиться номером телефона", request_contact=True)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_checkout_reply_keyboard(cake_name: str):
    builder = ReplyKeyboardBuilder()
    builder.button(text=f"Оформить заказ: {cake_name}")
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_cakes_keyboard():
    cakes_builder = ReplyKeyboardBuilder()
    cakes = db_manager.get_cakes()

    for cake in cakes:
        button_text = f"{cake['name']} - {cake['price']} руб."
        cakes_builder.add(KeyboardButton(text=button_text))

    cakes_builder.adjust(2)
    cakes_builder.row(KeyboardButton(text="Вернуться в главное меню"))

    return cakes_builder.as_markup(resize_keyboard=True)


