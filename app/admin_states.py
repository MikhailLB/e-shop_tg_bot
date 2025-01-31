from aiogram.fsm.state import State, StatesGroup


class MakeGood(StatesGroup):
    name = State()
    url = State()
    size = State()
    color = State()
    description = State()
    photo = State()
    price = State()
    category = State()
