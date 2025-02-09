from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from db.update_data import *
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

@router.callback_query(F.data == "back_to_main_menu")
async def find_item(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f"Привет, {callback.from_user.first_name}!\n"
                        f"Выбери нужную опцию!", reply_markup=kb.main_keyboard)


@router.callback_query(F.data == "back_to_main_menu_with_photo")
async def find_item(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f"Привет, {callback.from_user.first_name}!\n"
                        f"Выбери нужную опцию!", reply_markup=kb.main_keyboard)
    await callback.answer()



