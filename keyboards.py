from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import db_manager


def get_skip_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Пропустить")
    return builder.as_markup(resize_keyboard=True)


def get_main_menu_keyboard():
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.add(
        KeyboardButton(text="Посмотреть цены"),
        KeyboardButton(text="Заказать торт"),
        KeyboardButton(text="Собрать свой торт"),
        KeyboardButton(text="Мои заказы")
    )
    menu_builder.adjust(2)
    return menu_builder.as_markup(resize_keyboard=True)


def get_my_orders_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Посмотреть мои заказы"),
        KeyboardButton(text="Оплатить заказ"),
        KeyboardButton(text="Удалить заказ"),
        KeyboardButton(text="Оставить жалобу к заказу"),
        KeyboardButton(text="Вернуться в главное меню")
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_checkout_action_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Завершить оформление заказа"),
        KeyboardButton(text="Выбрать другой торт")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_final_checkout_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Поделиться номером телефона", request_contact=True),
        KeyboardButton(text="Оформить без телефона"),
        KeyboardButton(text="Вернуться в главное меню")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_checkout_reply_keyboard(cake_name: str):
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text=f"Оформить заказ: {cake_name}"),
        KeyboardButton(text="Выбрать другой торт")
    )
    builder.adjust(1)
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


