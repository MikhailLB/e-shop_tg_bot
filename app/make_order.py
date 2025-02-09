from datetime import datetime

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, PreCheckoutQuery
from aiogram.fsm.context import FSMContext
from amocrm_integration.post_order_to_crm import create_lead
from db.get_data import *
from keyboards.keyboards import main_keyboard

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
            [InlineKeyboardButton(text="✅ Все верно, продолжить", callback_data="confirm_order")],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")],
        ])

        await callback.message.edit_text(cart_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await callback.answer("Ваша корзина пуста!", show_alert=True)


@make_order_router.callback_query(F.data.startswith("confirm_order"))
async def make_order_check_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    items = get_cart_items(callback.from_user.id)
    for item in items:
        if items:
            name, description, size, color, price, img_url, product_id = item
            item = get_product_by_id(product_id)
            id, name1, url, size1, color1, description, price1 = item[0]
            info_about_user = get_info_about_account(user_id)
            firstname, surname, city, street, district, post_index, telephone, delivery_method = info_about_user
            address_cor = "Город: " + city + " | Улица: " + street + " | Район: " + district + " | Индекс: " + post_index
            create_lead(
                name=name,
                price=int(price),
                product_url=url,
                size=size,
                color=color,
                delivery_type=delivery_method,
                first_name=firstname,
                last_name=surname,
                phone=telephone,
                address=address_cor,
                date=datetime.today()
            )
    await callback.message.edit_text("Заказ принят и доступен для просмотра в 'Информация о заказе'", reply_markup=main_keyboard)
