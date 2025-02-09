from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📦 Управление товарами", callback_data="product_control"),
     InlineKeyboardButton(text="🧤 Управление заказами", callback_data="order_control")],
        [InlineKeyboardButton(text="🔃 Управление администраторами", callback_data="admin_control"), InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main_menu")],
])
admin_control_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить администратора", callback_data="add_admin"),
     InlineKeyboardButton(text="Удалить администратора", callback_data="delete_admin")],
        [InlineKeyboardButton(text="Назад", callback_data="get_back")],
])

orders_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Текущие заказы", callback_data="now_orders_kb"),
     InlineKeyboardButton(text="Выполненные заказы", callback_data="fulfill_orders")],
        [InlineKeyboardButton(text="Назад", callback_data="get_back")],
])

goods = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить товар", callback_data="add_product"),
     InlineKeyboardButton(text="Удалить товар", callback_data="delete_product")],
    [InlineKeyboardButton(text="Изменить товар", callback_data="add_product")],
        [InlineKeyboardButton(text="Назад", callback_data="get_back")],
])


get_admin_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="now_orders_kb")],
])

get_admin_back_to_mainmenu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="get_back")],
])