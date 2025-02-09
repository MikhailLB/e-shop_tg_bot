from aiogram import F, Router
from db.get_data import *
import keyboards.keyboards as kb
from keyboards.keyboards import back_menu

check_order_router = Router()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext

def get_orders_keyboard(index: int, total: int) -> InlineKeyboardMarkup:
    buttons = []
    if total > 1:
        buttons.append([
            InlineKeyboardButton(text="⏪", callback_data=f"prev_order_c|{index}"),
            InlineKeyboardButton(text=f"{index + 1}/{total}", callback_data="ignore"),
            InlineKeyboardButton(text="⏩", callback_data=f"next_order_c|{index + 1}")
        ])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@check_order_router.callback_query(F.data.startswith("info_about_order"))
async def make_order_check(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите опцию:", reply_markup=kb.check_order)

@check_order_router.callback_query(F.data.startswith("check_order"))
async def make_order_check_cart(callback: CallbackQuery, state: FSMContext):
    items = get_orders(callback.from_user.id)

    if items:
        index = 0
        total = len(items)

        name, price, delivery_method, size, color, address, order_status, tracking_link = items[index]

        text = (
            f"📦 Заказ №{index + 1}\n"
            f"Название: {name}\n"
            f"Цена: {price}₽\n"
            f"Доставка: {delivery_method}\n"
            f"Размер: {size}\n"
            f"Цвет: {color}\n"
            f"Адрес: {address}\n"
            f"Статус: {order_status}\n"
            f"Трекинг: {tracking_link if tracking_link else 'Как только мы обработаем заказ, появится трекинг-ссылка'}"
        )

        keyboard = get_orders_keyboard(index, total)
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer("У вас нет невыполненных заказов!", show_alert=True, reply_markup=back_menu)


@check_order_router.callback_query(F.data.startswith("prev_order_c"))
async def prev_order_c(callback: CallbackQuery, state: FSMContext):
    items = get_orders(callback.from_user.id)
    total = len(items)

    if total <= 1:
        await callback.answer("Доступен только один заказ.", show_alert=True)
        return

    index = int(callback.data.split("|")[1]) - 1
    if index < 0:
        index = total - 1

    await update_order_message(callback, items, index)

@check_order_router.callback_query(F.data.startswith("next_order_c"))
async def next_order_c(callback: CallbackQuery, state: FSMContext):
    items = get_orders(callback.from_user.id)
    total = len(items)

    if total <= 1:
        await callback.answer("Доступен только один заказ.", show_alert=True)
        return

    index = int(callback.data.split("|")[1])
    if index >= total:
        index = 0

    await update_order_message(callback, items, index)


async def update_order_message(callback: CallbackQuery, items, index: int):
    name, price, delivery_method, size, color, address, order_status, tracking_link = items[index]

    text = (
        f"📦 Заказ №{index + 1}\n"
        f"Название: {name}\n"
        f"Цена: {price}₽\n"
        f"Доставка: {delivery_method}\n"
        f"Размер: {size}\n"
        f"Цвет: {color}\n"
        f"Адрес: {address}\n"
        f"Статус: {order_status}\n"
        f"Трекинг: {tracking_link if tracking_link else 'Как только мы обработаем заказ, появится трекинг-ссылка'}"
    )

    keyboard = get_orders_keyboard(index, len(items))
    await callback.message.edit_text(text, reply_markup=keyboard)

@check_order_router.callback_query(F.data.startswith("check_all_orders"))
async def make_order_check_cart(callback: CallbackQuery, state: FSMContext):
    items = get_all_orders(callback.from_user.id)

    if items:
        index = 0
        total = len(items)

        name, price, delivery_method, size, color, address, order_status, tracking_link = items[index]

        text = (
            f"📦 Заказ №{index + 1}\n"
            f"Название: {name}\n"
            f"Цена: {price}₽\n"
            f"Доставка: {delivery_method}\n"
            f"Размер: {size}\n"
            f"Цвет: {color}\n"
            f"Адрес: {address}\n"
            f"Статус: {order_status}\n"
            f"Трекинг: {tracking_link if tracking_link else 'Как только мы обработаем заказ, появится трекинг-ссылка'}"
        )

        keyboard = get_orders_keyboard(index, total)
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer("У вас нет выполненных заказов!", show_alert=True, reply_markup=back_menu)


async def update_orders_message(callback: CallbackQuery, items, index: int):
    name, price, delivery_method, size, color, address, order_status, tracking_link = items[index]

    text = (
        f"📦 Заказ №{index + 1}\n"
        f"Название: {name}\n"
        f"Цена: {price}₽\n"
        f"Доставка: {delivery_method}\n"
        f"Размер: {size}\n"
        f"Цвет: {color}\n"
        f"Адрес: {address}\n"
        f"Статус: {order_status}\n"
        f"Трекинг: {tracking_link if tracking_link else 'Как только мы обработаем заказ, появится трекинг-ссылка'}"
    )

    keyboard = get_orders_keyboard(index, len(items))
    await callback.message.edit_text(text, reply_markup=keyboard)