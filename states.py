from aiogram.fsm.state import StatesGroup, State


class CatalogState(StatesGroup):
    waiting_for_cake = State()

class CustomCake(StatesGroup):
    wait_levels_cake = State()
    wait_form_cake = State()
    wait_topping_cake = State()
    wait_berries_cake = State()
    wait_decor_cake = State()
    wait_text_on_cake = State() 