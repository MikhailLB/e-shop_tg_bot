from aiogram.fsm.state import State, StatesGroup
from pydantic.v1.errors import cls_kwargs


class MakeGood(StatesGroup):
    name = State()
    url = State()
    size = State()
    color = State()
    description = State()
    photo = State()
    price = State()
    category = State()


class GetId(StatesGroup):
    id = State()
    name = State()