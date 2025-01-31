from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from db.category import categories
from db.get_data import *
import keyboards.keyboards as kb

user_product_index = {}
order_router = Router()

@order_router.message(F.text == "Оформление заказа")
async def make_order(message: Message):
    await message.answer("Выберите опцию:", reply_markup=kb.make_order_keyboard)


@order_router.callback_query(F.data == "find_product")
async def find_item(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите категорию:", reply_markup=kb.find_product_keyboard)


async def get_product_keyboard(category: str, index: int, total: int, product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏪", callback_data=f"prev_item|{category}|{index}"),
         InlineKeyboardButton(text=f"{index + 1}/{total}", callback_data="ignore"),
         InlineKeyboardButton(text="⏩", callback_data=f"next_item|{category}|{index}")],
        [InlineKeyboardButton(text="➕ Добавить в корзину", callback_data=f"add_to_cart|{product_id}")],
    ])

@order_router.callback_query(F.data == "find_product")
async def find_item(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите категорию:", reply_markup=kb.find_product_keyboard)

def generate_category_handler(category_name, callback_data):
    @order_router.callback_query(F.data == callback_data)
    async def category_handler(callback: CallbackQuery, state: FSMContext):
        products = get_products_by_category(category_name)

        if not products:
            await callback.message.edit_text(
                "⚠️ В этой категории нет товаров.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_find_product")]]
                )
            )
            return

        user_product_index = 0
        product = products[user_product_index]
        keyboard = await get_product_keyboard(category_name, user_product_index, len(products), product['id'])

        text = f"🛒 {product['name']}\n📖 {product['description']}\n📖 Размеры: {product['size']}\n📖 Цвета: {product['color']}\n💰 Цена: {product['price']} руб.\n"
        await callback.message.edit_media(media=InputMediaPhoto(media=product['photo_id'], caption=text),
                                          reply_markup=keyboard)

    return category_handler

@order_router.callback_query(F.data == "category_women_accessories")
async def women_accessories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите женские аксессуары:", reply_markup=kb.women_accessories_keyboard)

@order_router.callback_query(F.data == "category_men_accessories")
async def men_accessories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите мужские аксессуары:", reply_markup=kb.men_accessories_keyboard)

@order_router.callback_query(F.data == "category_menswear")
async def men_accessories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите мужскую одежду:", reply_markup=kb.menswear_keyboard)

@order_router.callback_query(F.data == "category_womenswear")
async def men_accessories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите женскую одежду:", reply_markup=kb.womenwear_keyboard)

@order_router.callback_query(F.data == "category_women_shoes")
async def women_shoes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите женскую обувь:", reply_markup=kb.women_shoes_keyboard)

@order_router.callback_query(F.data == "category_men_shoes")
async def men_shoes(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите мужскую обувь:", reply_markup=kb.men_shoes_keyboard)

@order_router.callback_query(F.data == "category_homewear")
async def homewear(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите тип домашней одежды:", reply_markup=kb.homewear_keyboard)

@order_router.callback_query(F.data == "category_sportwear")
async def sportwear(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите спортивную одежду:", reply_markup=kb.sportwear_keyboard)

@order_router.callback_query(F.data == "category_underwear")
async def underwear(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите нижнее белье:", reply_markup=kb.underwear_keyboard)

@order_router.callback_query(F.data == "category_swimwear")
async def swimwear(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите купальники и пляжную одежду:", reply_markup=kb.swimwear_keyboard)

@order_router.callback_query(F.data == "back_to_find_product")
async def back_to_find_product(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите категорию:", reply_markup=kb.find_product_keyboard)

@order_router.callback_query(F.data == "find_product")
async def find_item(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите категорию:", reply_markup=kb.find_product_keyboard)

@order_router.callback_query(F.data.startswith("prev_item") | F.data.startswith("next_item"))
async def navigate_products(callback: CallbackQuery, state: FSMContext):
    action, category, index = callback.data.split("|")
    index = int(index)
    products = get_products_by_category(category)

    if action == "next_item":
        index = (index + 1) % len(products)
    elif action == "prev_item":
        index = (index - 1) % len(products)

    product = products[index]
    keyboard = await get_product_keyboard(category, index, len(products), product['id'])
    text = f"🛒 {product['name']}\n📖 {product['description']}\n📖 Размеры: {product['size']}\n📖 Цвета: {product['color']}\n💰 Цена: {product['price']} руб.\n"
    await callback.message.edit_media(media=InputMediaPhoto(media=product['photo_id'], caption=text), reply_markup=keyboard)


for category, callback in categories.items():
    handler = generate_category_handler(category, callback)
    generate_category_handler(category, callback)
    order_router.callback_query(F.data == callback)(handler)