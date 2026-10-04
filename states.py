from aiogram.fsm.state import StatesGroup, State


class CatalogState(StatesGroup):
    waiting_for_cake = State()
    waiting_for_checkout_action = State()
    waiting_for_address = State()
    waiting_for_comment = State()
    waiting_for_delivery_date = State()
    waiting_for_delivery_time = State()
    waiting_for_pay_order_num = State()