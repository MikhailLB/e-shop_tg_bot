from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from db.update_data import *
from db.get_data import *
from app.states import *
import keyboards.keyboards as kb

user_product_index = {}
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\n"
                        f"Выбери нужную опцию!"
                        , reply_markup=kb.main_keyboard)
    user_id = message.from_user.id
    add_user(user_id)

@router.message(F.text == "Назад")
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись назад", reply_markup=kb.main_keyboard)






