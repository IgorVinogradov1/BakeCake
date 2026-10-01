from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from database import db_manager
import keyboards


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
        types.KeyboardButton(text="Не согласен, вернуться в меню")
    )
    pd_builder.adjust(1)
    
    await message.answer(
        "Для оформления заказа нам понадобятся ваши контактные данные (имя и телефон).\n"
        "Пожалуйста, подтвердите ваше согласие на обработку персональных данных",
        reply_markup=pd_builder.as_markup(resize_keyboard=True)
    )

@router.message(CommandStart())
async  def cmd_start(message: types.Message):
    db_manager.register_new_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )

    menu_builder = ReplyKeyboardBuilder()
    menu_builder.add(
        types.KeyboardButton(text="Посмотреть цены"),
        types.KeyboardButton(text="Заказать торт"),
        types.KeyboardButton(text="Собрать свой торт"),
        types.KeyboardButton(text="Мои заказы")
    )
    menu_builder.adjust(2)

    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        f"Добро пожаловать в BakeCake. Здесь можно заказать самый вкусный торт!\n\n",
        reply_markup=menu_builder.as_markup(resize_keyboard=True)
    )

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
    if db_manager.has_user_agreed(message.from_user.id):
        await message.answer(
        "Приступим к заказу!",
        reply_markup=ReplyKeyboardRemove()
        )
    else:
        await send_agreement(message)


@router.message(F.text == "Согласен, продолжить заказ")
async def process_pd_agree(message: types.Message):
    db_manager.save_user_agreement(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    await message.answer(
        "Отлично! Приступим к заказу!",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(F.text == "Не согласен, вернуться в меню")
async def process_pd_disagree(message: types.Message):
    await message.answer("К сожалению, без согласия на обработку данных мы не сможем принять ваш заказ.")
    await cmd_start(message)


@router.message(F.text == "Заказать торт")
async def order_cake(message: types.Message):
    if db_manager.has_user_agreed(message.from_user.id):
        await message.answer(
        "Выберите один из наших готовых тортов.",
        reply_markup=keyboards.get_cakes_keyboard())
    else:
        await send_agreement(message)

        
@router.message()
async def process_cake_selection(message: types.Message):
    cakes = db_manager.get_cakes()

    selected_cake = None
    for cake in cakes:
        if message.text.startswith(cake["name"]):
            selected_cake = cake
            break

    if selected_cake:
        await message.answer(
            f"В вашей корзине {selected_cake['name']}\n"
            f"Сумма заказа {selected_cake['price']}"
        )
    else:
        await message.answer("Пожалуйста, выберете торт нажав на одну из кнопок!")