from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async  def cmd_start(message: types.Message):
    # Тут позже будет логика на проверку согласия она ПД
    # Если да - пускаем в меню
    # Если нет? - прогоняем? даем рекламу? Сообщения ждем вас снова?

    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        f"Добро пожаловать в BakeCake. Здесь можно заказать самый вкусный торт!\n\n"
    )