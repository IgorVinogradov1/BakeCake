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
        KeyboardButton(text="Добавить комментарий к заказу"),
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

def get_levels_cake_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="1 уровень (+400р.)"),
        KeyboardButton(text="2 уровня (+750р.)"),
        KeyboardButton(text="3 уровня (+1100р.)"),
        KeyboardButton(text="Отменить сборку и вернуться в главное меню")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_form_cake_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Круг (+400р.)"),
        KeyboardButton(text="Квадрат (+600р.)"),
        KeyboardButton(text="Прямоугольник (+1000р.)"),
        KeyboardButton(text="Отменить сборку и вернуться в главное меню")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_topping_cake_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Без топпинга (+0р.)"),
        KeyboardButton(text="Белый соус (+200р.)"),
        KeyboardButton(text="Карамельный сироп (+180р.)"),
        KeyboardButton(text="Кленовый сироп (+200р.)"),
        KeyboardButton(text="Клубничный сироп (+300р.)"),
        KeyboardButton(text="Черничный сироп (+350р.)"),
        KeyboardButton(text="Молочный шоколад (+200р.)"),
        KeyboardButton(text="Отменить сборку и вернуться в главное меню")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_berries_cake_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Без ягод (+0р.)"),
        KeyboardButton(text="Ежевика (+400р.)"),
        KeyboardButton(text="Малина (+300р.)"),
        KeyboardButton(text="Голубика (+450р.)"),
        KeyboardButton(text="Клубника (+500р.)"),
        KeyboardButton(text="Отменить сборку и вернуться в главное меню")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_decor_cake_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Без декора (+0р.)"),
        KeyboardButton(text="Фисташки (+300р.)"),
        KeyboardButton(text="Безе (+400р.)"),
        KeyboardButton(text="Фундук (+350р.)"),
        KeyboardButton(text="Пекан (+300р.)"),
        KeyboardButton(text="Маршмеллоу (+200р.)"),
        KeyboardButton(text="Марципан (+280р.)"),
        KeyboardButton(text="Отменить сборку и вернуться в главное меню")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_text_on_cake_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Без надписи на торте (+0р.)"),
        KeyboardButton(text="Отменить сборку и вернуться в главное меню")
    )
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)