from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from database import db_manager
import keyboards
import os

from states import CatalogState

router = Router()


async def send_agreement(message: types.Message):
    pdf_file = FSInputFile("agreement.pdf")
    await message.answer_document(
        document=pdf_file,
        caption="Ознакомьтесь с Соглашением на обработку персональных данных."
    )
    pd_builder = ReplyKeyboardBuilder()
    pd_builder.add(
        types.KeyboardButton(text="Согласен, продолжить заказ"),
        types.KeyboardButton(text="Не согласен")
    )
    pd_builder.adjust(1)
    await message.answer(
        "Для оформления заказа нам понадобятся ваши контактные данные (имя и телефон).\n"
        "Пожалуйста, подтвердите ваше согласие на обработку персональных данных",
        reply_markup=pd_builder.as_markup(resize_keyboard=True)
    )


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    db_manager.register_new_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        f"Добро пожаловать в BakeCake. Здесь можно заказать самый вкусный торт!\n\n",
    )

    if db_manager.has_user_agreed(message.from_user.id):
        await message.answer(
            f"Выберете интересующий пункт меню:",
            reply_markup=keyboards.get_main_menu_keyboard()
        )
    else:
        await send_agreement(message)


@router.message(F.text == "Посмотреть цены")
async def show_prices(message: types.Message):
    await message.answer(
        "**Наши цены:**\n"
        "Классические торты — от 1500 руб.\n"
        "Праздничные торты — от 2200 руб/кг.\n\n"
        "Для заказа нажмите на кнопку 'Заказать торт' в меню."
    )


@router.message(F.text == "Собрать свой торт")
async def constructor_cake(message: types.Message):
    await message.answer(
        "Приступим к заказу!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text == "Согласен, продолжить заказ")
async def process_pd_agree(message: types.Message):
    db_manager.save_user_agreement(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    await message.answer(
        "Отлично! Приступим к заказу?",
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@router.message(F.text == "Мои заказы")
async def show_my_orders_menu(message: types.Message):
    await message.answer(
        "Управление вашими заказами",
        reply_markup=keyboards.get_my_orders_keyboard()
    )


@router.message(F.text == "Посмотреть мои заказы")
async def process_show_orders(message: types.Message):
    user_id = message.from_user.id
    orders_list = db_manager.show_orders(user_id)
    if orders_list:
        await message.answer(
            "Ваши заказы :\n\n" + "\n\n".join(orders_list)
        )
    else:
        await message.answer(
            "У вас еще нет заказов"
        )


@router.message(F.text == "Удалить последний заказ")
async def process_delete_order(message: types.Message):
    user_id = message.from_user.id
    delete_order = db_manager.cancel_last_order(user_id)
    if delete_order:
        await message.answer(
            "Ваш заказ успешно удален"
        )
    else:
        await message.answer(
            "У вас больше нет заказов"
        )


@router.message(F.text == "Заказать торт")
async def order_cake(message: types.Message, state: FSMContext):
    await state.set_state(CatalogState.waiting_for_cake)
    await message.answer(
        "Выберите один из наших готовых тортов.",
        reply_markup=keyboards.get_cakes_keyboard()
    )


@router.message(F.text == "Не согласен")
async def process_pd_disagree(message: types.Message):
    await message.answer(
        "К сожалению, без согласия на обработку данных мы не сможем принять ваш заказ.",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.contact)
async def process_phone_contact(message: types.Message):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id

    db_manager.update_last_order_data(user_id, phone_number)

    await message.answer(
        "Спасибо за заказ!\n"
        "В ближайшее время с вами свяжется наш менеджер.\n"
        "Добавить комментарий к заказу, посмотреть свои заказы или удалить заказ\n "
        "Вы можете в меню 'МОИ ЗАКАЗЫ'.",
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@router.message(F.text == "Выбрать другой торт")
async def process_cancel_and_cake_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    db_manager.cancel_last_order(user_id)
    await state.set_state(CatalogState.waiting_for_cake)

    await message.answer(
        "Заказ отменен. Выбираем другой торт.",
        reply_markup=keyboards.get_cakes_keyboard()
    )


@router.message(F.text == "Оформить без телефона")
async def process_checkout_without_phone(message: types.Message):
    customer_name = message.from_user.first_name
    await message.answer(
        "Ваш заказ успешно подтвержден!\n"
        "Добавить комментарий к заказу, посмотреть свои заказы или удалить заказ\n "
        "Вы можете в меню 'МОИ ЗАКАЗЫ'.",
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@router.message(F.text == "Вернуться в главное меню")
async def back_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await cmd_start(message)


@router.message(F.text.startswith("Оформить заказ:"), CatalogState.waiting_for_cake)
async def process_checkout_click(message: types.Message, state: FSMContext):
    await state.clear()
    cake_name_from_button = message.text.replace("Оформить заказ: ", "")

    cakes = db_manager.get_cakes()
    selected_cake = None
    for cake in cakes:
        if cake["name"] == cake_name_from_button:
            selected_cake = cake
            break

    customer_name = message.from_user.first_name
    user_id = message.from_user.id
    if message.from_user.username:
        tg_username = f"@{message.from_user.username}"
    else:
        tg_username = f"{user_id}"

    db_manager.save_cake_order(
        user_id=user_id,
        cake_name=selected_cake["name"],
        cake_price=selected_cake["price"],
        customer_name=customer_name,
        customer_phone=None,
        tg_username=tg_username,
    )
    await message.answer(
        f"{customer_name}, Ваш заказ: торт {selected_cake['name']} принят!\n"
        f"Сумма вашего заказа {selected_cake['price']}!\n",
        reply_markup=keyboards.get_checkout_action_keyboard()
    )

@router.message(F.text == "Завершить оформление заказа")
async def process_final_step(message: types.Message, state: FSMContext):
    await  state.set_state(CatalogState.waiting_for_address)
    await  message.answer(
        "Пожалуйста напишите адрес доставки!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(CatalogState.waiting_for_address)
async def process_address_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_address = message.text
    db_manager.update_last_order_data(user_id=user_id, address=user_address)
    await state.set_state(CatalogState.waiting_for_comment)
    await message.answer(
        "Адрес успешно сохранен в ваш заказ\n"
        "Оставьте комментарий к заказу",
        reply_markup=keyboards.get_skip_keyboard()
    )


@router.message(CatalogState.waiting_for_comment)
async def process_comment_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text == "Пропустить":
        user_comment = message.text
    else:
        user_comment = message.text

    db_manager.update_last_order_data(user_id=user_id, comment=user_comment)
    await state.set_state(CatalogState.waiting_for_delivery_date)
    await message.answer(
        "Пожалуйста укажите желаемою дату доставки в формате дд.мм.гггг\n"
        "Например, 10.10.2026\n"
        "Если дата доставки в ближайшие 24 часа + 20% к стоимости заказа!"
    )
@router.message(CatalogState.waiting_for_delivery_date)
async def process_delivery_date_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    date_text = message.text

    db_manager.update_last_order_data(user_id=user_id, delivery_date=date_text)
    await state.clear()

    await message.answer(
        "Последний штрих к оформлению вашего заказа\n",
        reply_markup=keyboards.get_final_checkout_keyboard()
    )


@router.message(F.text == "Выбрать другой торт")
async def back_to_cake_menu(message: types.Message, state: FSMContext):
    await state.set_state(CatalogState.waiting_for_cake)
    await message.answer(
        "Выбрать другой торт",
        reply_markup=keyboards.get_cakes_keyboard()
    )


@router.message(CatalogState.waiting_for_cake)
async def process_cake_selection(message: types.Message, state: FSMContext):

    cakes = db_manager.get_cakes()

    selected_cake = None
    for cake in cakes:
        if message.text.startswith(cake["name"]):
            selected_cake = cake
            break

    if selected_cake:

        caption_text = selected_cake["description"]
        image_path = selected_cake.get("img")

        checkout_kb = keyboards.get_checkout_reply_keyboard(selected_cake["name"])

        if image_path and os.path.exists(image_path):
            cake_img = FSInputFile(image_path)
            await message.answer_photo(
                photo=cake_img,
                caption=caption_text,
                reply_markup=checkout_kb
            )
        else:
            text_fallback = (
                f"{caption_text}\n"
                f"Упс, мы временно потеряли фото этого торта =/"
            )
            await message.answer(
                text=text_fallback,
                reply_markup=checkout_kb
            )
    else:
        await message.answer("Пожалуйста, выберете торт нажав на одну из кнопок!")
