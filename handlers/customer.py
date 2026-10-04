from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from database import db_manager
import keyboards
import os

from states import CatalogState, CustomCake

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
    await message.answer_document(
        document=FSInputFile("сakes_catalog.xlsx"),
        caption="Ознакомьтесь с нашим каталогом готовых тортов.",
        reply_markup=keyboards.get_main_menu_keyboard()
    )


@router.message(F.text == "Отменить сборку и вернуться в главное меню", CustomCake())
async def cancel_custom_cake(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Сборка торта отменена!", reply_markup=ReplyKeyboardRemove())
    await cmd_start(message)


@router.message(F.text == "Собрать свой торт")
async def constructor_cake(message: types.Message, state: FSMContext):
    await state.set_state(CustomCake.wait_levels_cake)
    await state.update_data(total_price=0)
    await message.answer(
        "Приступим к сборке!\nВыберите количество уровней:",
        reply_markup=keyboards.get_levels_cake_keyboard()
    )


@router.message(CustomCake.wait_levels_cake, F.text.contains("(+"))
async def process_levels(message: types.Message, state: FSMContext):
    price = int(message.text.split("(+")[1].replace("р.)", ""))
    data = await state.get_data()
    
    await state.update_data(
        levels=message.text.split(" (+")[0],
        total_price=data["total_price"] + price
    )
    await state.set_state(CustomCake.wait_form_cake)
    await message.answer("Отлично. Теперь выберите форму торта:", reply_markup=keyboards.get_form_cake_keyboard())


@router.message(CustomCake.wait_form_cake, F.text.contains("(+"))
async def process_form_cake(message: types.Message, state: FSMContext):
    price = int(message.text.split("(+")[1].replace("р.)", ""))
    data = await state.get_data()
    
    await state.update_data(
        shape=message.text.split(" (+")[0],
        total_price=data["total_price"] + price
    )
    await state.set_state(CustomCake.wait_topping_cake)
    await message.answer("Выберите топпинг для торта:", reply_markup=keyboards.get_topping_cake_keyboard())


@router.message(CustomCake.wait_topping_cake, F.text.contains("(+"))
async def process_topping(message: types.Message, state: FSMContext):
    price = int(message.text.split("(+")[1].replace("р.)", ""))
    data = await state.get_data()

    await state.update_data(
        topping=message.text.split(" (+")[0],
        total_price=data["total_price"] + price
    )
    await state.set_state(CustomCake.wait_berries_cake)
    await message.answer("Добавить ягоды?", reply_markup=keyboards.get_berries_cake_keyboard())


@router.message(CustomCake.wait_berries_cake, F.text.contains("(+"))
async def process_berries(message: types.Message, state: FSMContext):
    price = int(message.text.split("(+")[1].replace("р.)", ""))
    data = await state.get_data()

    await state.update_data(
        berries=message.text.split(" (+")[0],
        total_price=data["total_price"] + price
    )
    await state.set_state(CustomCake.wait_decor_cake)
    await message.answer("Добавить декор?", reply_markup=keyboards.get_decor_cake_keyboard())


@router.message(CustomCake.wait_decor_cake, F.text.contains("(+"))
async def process_decor(message: types.Message, state: FSMContext):
    price = int(message.text.split("(+")[1].replace("р.)", ""))
    data = await state.get_data()

    await state.update_data(
        decor=message.text.split(" (+")[0],
        total_price=data["total_price"] + price
    )
    await state.set_state(CustomCake.wait_text_on_cake)
    await message.answer(
        "Мы можем разместить на торте любую надпись.\n"
        "Введите желаемый текст сообщением (стоимость надписи +500р.) или выберете без надписи.",
        reply_markup=keyboards.get_text_on_cake_keyboard()
    )


@router.message(CustomCake.wait_text_on_cake)
async def process_constructor_final(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    if message.text == "Без надписи на торте (+0р.)":
        cake_text = "без надписи"
        final_price = data["total_price"]
    elif message.text == "Отменить сборку и вернуться в главное меню":
        await cancel_custom_cake(message, state)
        return
    else:
        cake_text = f"«{message.text}»"
        final_price = data["total_price"] + 500

    cake_description = f"Заказной ({data['levels']}; {data['shape']}; Топпинг: {data['topping']}; Ягоды: {data['berries']}; Декор: {data['decor']}; Надпись: {cake_text})"

    customer_name = message.from_user.first_name
    user_id = message.from_user.id
    tg_username = f"@{message.from_user.username}" if message.from_user.username else f"{user_id}"


    db_manager.save_cake_order(
        user_id=user_id,
        cake_name=cake_description,
        cake_price=final_price,
        customer_name=customer_name,
        customer_phone=None,
        tg_username=tg_username,
    )
    
    await state.clear()
    
    await message.answer(
        f"{customer_name}, Ваш уникальный торт собран и принят!\n"
        f"Итоговая стоимость: {final_price} руб.!\n"
        f"Поделитесь своим номером для связи с вами!",
        reply_markup=keyboards.get_checkout_action_keyboard()
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
        await message.answer("Ваши заказы:\n\n" + "\n\n".join(orders_list))
    else:
        await message.answer("У вас еще нет заказов")


@router.message(F.text == "Удалить заказ")
async def process_delete_order_start(message: types.Message, state: FSMContext):
    await state.set_state(CatalogState.waiting_for_delete_order_num)
    await message.answer(
        "Пожалуйста, введите номер заказа, который вы хотите удалить:",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(CatalogState.waiting_for_delete_order_num)
async def verify_delete_order_num(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный номер заказа (только цифры):")
        return

    user_id = message.from_user.id
    order_num = int(message.text)
    await state.clear()

    if db_manager.delete_order(user_id, order_num):
        await message.answer(
            f"Заказ № {order_num} успешно удален.",
            reply_markup=keyboards.get_my_orders_keyboard()
        )
    else:
        await message.answer(
            f"Заказ № {order_num} не найден среди ваших заказов.\n",
            reply_markup=keyboards.get_my_orders_keyboard()
        )


@router.message(F.text == "Оплатить заказ")
async  def process_pay_order(message: types.Message, state: FSMContext):
    await  state.set_state(CatalogState.waiting_for_pay_order_num)

    await message.answer(
        "Пожалуйста, введите номер заказа, который хотите оплатить",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(CatalogState.waiting_for_pay_order_num)
async def confirm_pay_order(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите номер заказа")
        return

    user_id = message.from_user.id
    order_num = int(message.text)

    await  state.clear()

    order =db_manager.get_order_by_num(user_id, order_num)
    if order:
        cake_name = order["cake_name"]
        price = order["cake_price"]

        receipt_text = (
            f"Чек на оплату заказа № {order_num}\n"
            f"Торт {cake_name}\n"
            f"Сумма к оплате {price}\n"
            f"Для оплаты перейдите по ссылке\n"
            f"https://nspk.ru{order_num}_price{price}\n\n"
        )

        await  message.answer(
            text=receipt_text,
            parse_mode="HTML",
            reply_markup=keyboards.get_my_orders_keyboard()
        )
    else:
        await message.answer(
            f"Заказ № {order_num} не найден среди ваших заказов.\n",
            reply_markup=keyboards.get_my_orders_keyboard()
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
        "Добавить комментарий к заказу, посмотреть или удалить заказ\n"
        "Вы можете в меню «Мои заказы».",
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
        "Добавить комментарий к заказу, посмотреть или удалить заказ\n"
        "Вы можете в меню «Мои заказы».",
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
        "Пожалуйста, напишите адрес доставки!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(CatalogState.waiting_for_address)
async def process_address_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_address = message.text
    db_manager.update_last_order_data(user_id=user_id, address=user_address)
    await state.set_state(CatalogState.waiting_for_comment)
    await message.answer(
        "Адрес успешно сохранен в ваш заказ.\n"
        "Вы можете оставить комментарий к заказу:",
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
        "Пожалуйста, укажите желаемую дату доставки в формате дд.мм.гггг. "
        "Например, 10.10.2026.\n"
        "Если дата доставки в ближайшие 24 часа + 20% к стоимости заказа!",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(CatalogState.waiting_for_delivery_date)
async def process_delivery_date_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    date_text = message.text

    db_manager.update_last_order_data(user_id=user_id, delivery_date=date_text)

    await state.set_state(CatalogState.waiting_for_delivery_time)

    await message.answer(
        "Пожалуйста, укажите желаемое время доставки!\n",
        reply_markup=keyboards.get_skip_keyboard()
    )


@router.message(CatalogState.waiting_for_delivery_time)
async def process_delivery_time_output(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    delivery_time_text = message.text

    db_manager.update_last_order_data(user_id=user_id, delivery_time=delivery_time_text)

    await state.clear()
    await message.answer(
        "Последний штрих к оформлению вашего заказа.",
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