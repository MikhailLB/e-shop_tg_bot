from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from app.states import *
from db.get_data import *
import keyboards.keyboards as kb
from db.update_data import update_user_data, delete_user_data

make_order_router = Router()


@make_order_router.callback_query(F.data.startswith("make_order_continue"))
async def make_order_check_cart(callback: CallbackQuery, state: FSMContext):
    items = get_cart_items(callback.from_user.id)
    if items:
        total_price = 0
        cart_text = "🛒 Ваш заказ:\n\n"

        for item in items:
            name, description, size, color, price, img_url, product_id = item
            cart_text += f"<b>Название: {name}\nРазмер: {size}\nЦвет: {color}\nЦена: {price}₽\n\n</b>"
            total_price += price

        cart_text += f"\n<b>Итого: {total_price}₽</b>"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Все верно, продолжить", callback_data="confirm_order")]
        ])

        await callback.message.edit_text(cart_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await callback.answer("Ваша корзина пуста!", show_alert=True)
