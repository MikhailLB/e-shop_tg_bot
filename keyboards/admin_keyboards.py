from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="🛠 Управление ботом")],
        [KeyboardButton(text="📦 Управление товарами"), KeyboardButton(text="👤 Управление пользователями")]
    ],
    resize_keyboard=True
)
goods = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить товар"), KeyboardButton(text="Изменить товар")],
        [KeyboardButton(text="Удалить товар")],
    ],
    resize_keyboard=True
)
