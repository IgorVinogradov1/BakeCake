from aiogram.fsm.state import StatesGroup, State


class CatalogState(StatesGroup):
    waiting_for_cake = State()
    waiting_for_checkout_action = State()
    waiting_for_address = State()
    waiting_for_comment = State()
    waiting_for_delivery_date = State()
    waiting_for_delivery_time = State()
    waiting_for_pay_order_num = State()
    waiting_for_delete_order_num = State()

class CustomCake(StatesGroup):
    wait_levels_cake = State()
    wait_form_cake = State()
    wait_topping_cake = State()
    wait_berries_cake = State()
    wait_decor_cake = State()
    wait_text_on_cake = State() 