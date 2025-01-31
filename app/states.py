from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.testing.assertsql import SQLAsserter


class MakeOrder(StatesGroup):
    link = State()
    user_id = State()
    price = State()
    name = State()

class RegPost(StatesGroup):
    name = State()
    second_name = State()
    city = State()
    street = State()
    district = State()
    index = State()
    telephone = State()
    delivery_method = State()
class RegCurr(StatesGroup):
    name = State()
    second_name = State()
    city = State()
    street = State()
    district = State()
    index = State()
    telephone = State()
    delivery_method = State()
class PostReview(StatesGroup):
    stars = State()
    comment = State()

class AddToCart(StatesGroup):
    size = State()
    color = State()