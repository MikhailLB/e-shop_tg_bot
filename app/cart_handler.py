from itertools import product

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.get_data import *
import keyboards.keyboards as kb
from db.update_data import add_cart_to_db, delete_cart_item

user_product_index = {}
cart_router = Router()


async def get_cart_keyboard(index: int, total: int,) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⏪", callback_data=f"prev_cart_item|{index}"),
            InlineKeyboardButton(text=f"{index + 1}/{total}", callback_data="ignore"),
            InlineKeyboardButton(text="⏩", callback_data=f"next_cart_item|{index+1}")
        ],
        [
            InlineKeyboardButton(text="🛒 Оформить заказ", callback_data="checkout_order")
        ],
        [
            InlineKeyboardButton(text="❌ Удалить", callback_data=f"remove_from_cart|{index}")
        ]
    ])



def generate_size_keyboard(sizes: str, product_id: int, selected_size: str = None) -> InlineKeyboardMarkup:
    size_list = sizes.split()
    keyboard = InlineKeyboardBuilder()

    for size in size_list:
        if size != selected_size:
            keyboard.button(text=size, callback_data=f"select_size|{product_id}|{size}")

    keyboard.adjust(3)
    return keyboard.as_markup()


def generate_color_keyboard(colors: str, product_id: int, size: str) -> InlineKeyboardMarkup:
    color_list = colors.split()
    keyboard = InlineKeyboardBuilder()

    for color in color_list:
        keyboard.button(text=color, callback_data=f"select_color|{product_id}|{size}|{color}")

    keyboard.adjust(3)
    return keyboard.as_markup()


@cart_router.callback_query(F.data.startswith("add_to_cart"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("|")[1])
    item = find_item_in_cart(product_id, callback.from_user.id)
    if not item:
        product = get_products_by_id(product_id)[0]

        size_keyboard = generate_size_keyboard(product[3], product_id)

        await callback.message.edit_media(
            media=InputMediaPhoto(media=product[2], caption="Выберите размер:"),
            reply_markup=size_keyboard
        )

        await callback.answer("✅ Выберите размер товара!")
    else:
        await callback.answer("✅ Товар уже есть в корзине!")


@cart_router.callback_query(F.data.startswith("select_size"))
async def select_size(callback: CallbackQuery, state: FSMContext):
    _, product_id, size = callback.data.split("|")

    product = get_products_by_id(int(product_id))[0]

    await state.update_data(product_id=int(product_id), size=size)

    color_keyboard = generate_color_keyboard(product[4], int(product_id), size)

    await callback.message.edit_media(
        media=InputMediaPhoto(media=product[2], caption=f"✅ Размер {size} выбран!\nТеперь выберите цвет:"),
        reply_markup=color_keyboard
    )

    await callback.answer(f"✅ Размер {size} выбран!")



@cart_router.callback_query(F.data.startswith("select_color"))
async def select_color(callback: CallbackQuery, state: FSMContext):
    _, product_id, size, color = callback.data.split("|")

    user_data = await state.get_data()
    product_id = user_data["product_id"]
    size = user_data["size"]

    product = get_products_by_id(int(product_id))[0]
    try:
        add_cart_to_db(callback.from_user.id, product[1], product[2], size, color, product[5], product[6], product[7], product[0])

        await callback.message.edit_media(
            media=InputMediaPhoto(media=get_products_by_id(int(product_id))[0][2],
                                  caption=f"✅ Товар добавлен в корзину!\nРазмер: {size}\nЦвет: {color}")
        )
        await callback.answer("🎉 Товар успешно добавлен в корзину!")
    except Exception as e:
        await callback.answer("Не удалось добавить товар в корзину!")


@cart_router.message(F.text == "Корзина")
async def cart(message: Message, state: FSMContext):
    await state.clear()
    items = get_cart_items(message.from_user.id)

    if not items:
        await message.answer("🛒 Ваша корзина пуста!")
        return

    index = 0
    await state.update_data(cart_items=items, cart_index=index)

    name, description, size, color, price, url, product_id = items[index]
    await message.answer_photo(
        photo=url,
        caption=f"<b>{name}</b>\n\n"
                f"📄 Описание: {description if description else 'Нет описания'}\n"
                f"💰 Цена: {price} ₽\n"
                f"📏 Размер: {size}\n"
                f"🎨 Цвет: {color}",
        reply_markup=await get_cart_keyboard(index, len(items)),
        parse_mode="HTML"
    )


@cart_router.callback_query(F.data.startswith("prev_cart_item"))
async def prev_cart_item(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    items = data.get("cart_items", [])
    index = data.get("cart_index", 0)

    if len(items) <= 1:
        await callback.answer("В корзине только один товар")
        return

    index = (index - 1) % len(items)
    await state.update_data(cart_index=index)

    name, description, size, color, price, url, product_id = items[index]
    await callback.message.edit_media(
        media=InputMediaPhoto(media=url, caption=f"<b>{name}</b>\n\n"
                                                 f"📄 Описание: {description if description else 'Нет описания'}\n"
                                                 f"💰 Цена: {price} ₽\n"
                                                 f"📏 Размер: {size}\n"
                                                 f"🎨 Цвет: {color}", parse_mode="HTML"),
        reply_markup=await get_cart_keyboard(index, len(items))
    )


@cart_router.callback_query(F.data.startswith("next_cart_item"))
async def next_cart_item(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    items = data.get("cart_items", [])
    index = data.get("cart_index", 0)

    if len(items) <= 1:
        await callback.answer("В корзине только один товар")
        return

    index = (index + 1) % len(items)
    await state.update_data(cart_index=index)

    name, description, size, color, price, url, product_id = items[index]
    await callback.message.edit_media(
        media=InputMediaPhoto(media=url, caption=f"<b>{name}</b>\n\n"
                                                 f"📄 Описание: {description if description else 'Нет описания'}\n"
                                                 f"💰 Цена: {price} ₽\n"
                                                 f"📏 Размер: {size}\n"
                                                 f"🎨 Цвет: {color}", parse_mode="HTML"),
        reply_markup=await get_cart_keyboard(index, len(items))
    )


@cart_router.callback_query(F.data.startswith("remove_from_cart"))
async def remove_from_cart(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    items = data.get("cart_items", [])
    index = data.get("cart_index", 0)

    if not items:
        await callback.answer("🛒 Ваша корзина уже пуста!")
        return

    _, _, _, _, _, _, product_id = items[index]

    delete_cart_item(callback.from_user.id, product_id)

    items = get_cart_items(callback.from_user.id)

    await state.update_data(cart_items=items, cart_index=min(index, len(items) - 1))

    await callback.answer("❌ Товар удален из корзины!")
