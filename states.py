from aiogram.fsm.state import StatesGroup, State


class CatalogState(StatesGroup):
    waiting_for_cake = State()