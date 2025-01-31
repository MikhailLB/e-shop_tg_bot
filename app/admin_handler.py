from aiogram import Router, F
from aiogram.types import Message
from keyboards.admin_keyboards import *
import openpyxl
from aiogram import types
from aiogram.filters import Command
from db.update_data import insert_products
from db.get_data import *
ADMINS = {1272027592}
admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    user_id = message.from_user.id

    if user_id in ADMINS:
        await message.answer("🔹 Добро пожаловать в панель администратора!", reply_markup=admin_keyboard)
    else:
        await message.answer("⛔ У вас нет доступа к этой команде.")

@admin_router.message(F.text == "📦 Управление товарами")
async def admin_panel(message: Message):
    user_id = message.from_user.id

    if user_id in ADMINS:
        await message.answer("🔹 Управление товарами", reply_markup=goods)
    else:
        await message.answer("⛔ У вас нет доступа к этой команде.")

@admin_router.message(F.text == "Добавить товар")
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        await message.answer("Отправьте Excel файл со следующими колонками: name, url, size, color, description, photo_url, price, category")
    else:
        await message.answer("⛔ У вас нет доступа к этой команде.")

@admin_router.message(lambda message: message.document and message.document.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
async def handle_excel(message: types.Message):
    document = message.document
    file_path = f"data.xlsx"

    file = await message.bot.get_file(document.file_id)
    await message.bot.download_file(file.file_path, file_path)

    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active

        headers = [cell.value for cell in sheet[1] if cell.value]

        required_columns = ["name", "url", "size", "color", "description", "photo_url", "price", "category"]
        if not all(col in headers for col in required_columns):
            await message.answer("Ошибка: В файле отсутствуют необходимые колонки!")
            return

        data_list = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data_list.append(list(row))

        goods = check_existing_products(data_list)
        if goods:
            await message.answer(f"Товары уже существуют!\nСуществующие товары: ")
            for i in goods:
                await message.answer(f"{i[1]}\n{i[2]}")

        else:
            insert_products(data_list)
            await message.answer(f"Товары добавлены в БД")

    except Exception as e:
        await message.answer(f"Ошибка при обработке файла: {e}")



# @admin_router.message(F.text == 'Добавить товар')
# async def add_good(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id in ADMINS:
#         await message.answer("Введите название товара\nОно должно быть уникальным!\nЧтобы по нему был возможен поиск, оно должно быть точь в точь как на poizon")
#         await state.set_state(MakeGood.name)
#         await state.update_data(name=message.text)
#         await state.set_state(MakeGood.url)
#     else:
#         await message.answer("⛔ У вас нет доступа к этой команде.")
#
# @admin_router.message(MakeGood.url)
# async def add_good1(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id in ADMINS:
#         await message.answer("Введите url товара:")
#         await state.update_data(url=message.text)
#         await state.set_state(MakeGood.size)
#     else:
#         await message.answer("⛔ У вас нет доступа к этой команде.")
#
# @admin_router.message(MakeGood.size)
# async def add_good2(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id in ADMINS:
#         await message.answer("Введите размеры товара в одну строку через пробел: ")
#         try:
#             sizes = message.text.split(" ")
#             await state.update_data(size=sizes)
#             await state.set_state(MakeGood.color)
#         except:
#             await message.answer("Произошла ошибка, попробуйте еще раз")
#     else:
#         await message.answer("⛔ У вас нет доступа к этой команде.")
#
# @admin_router.message(MakeGood.color)
# async def add_good3(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id in ADMINS:
#         await message.answer("Введите цвета товара в одну строку через пробел: ")
#         try:
#             colors = message.text.split(" ")
#             await state.update_data(color=colors)
#             await state.set_state(MakeGood.description)
#         except:
#             await message.answer("Произошла ошибка, попробуйте еще раз")
#     else:
#         await message.answer("⛔ У вас нет доступа к этой команде.")
#
# @admin_router.message(MakeGood.description)
# async def add_good4(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id in ADMINS:
#         await message.answer("Введите описание товара: ")
#         await state.update_data(description=message.text)
#         await state.set_state(MakeGood.photo)
#     else:
#         await message.answer("⛔ У вас нет доступа к этой команде.")
#
#
# @admin_router.message(MakeGood.photo)
# async def add_good5(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id in ADMINS:
#         await message.answer("Отправьте фото товара: ")
#         try:
#             last_uploaded_photo_id = message.photo[-1].file_id
#             print(last_uploaded_photo_id)
#             await state.update_data(photo=last_uploaded_photo_id)
#             await state.set_state(MakeGood.price)
#         except:
#             await message.answer("Не удалось загрузить фото")
#     else:
#         await message.answer("⛔ У вас нет доступа к этой команде.")
#
# @admin_router.message(MakeGood.price)
# async def add_good6(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id in ADMINS:
#         await message.answer("Введите цену товара (только число без валюты): ")
#         await state.update_data(price=message.text)
#         await state.set_state(MakeGood.category)
#     else:
#         await message.answer("⛔ У вас нет доступа к этой команде.")
#
#
# @admin_router.message(MakeGood.category)
# async def add_good8(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if user_id in ADMINS:
#         await message.answer("Выберите категорию товара",reply_markup=kb.find_product_keyboard)
#     else:
#         await message.answer("⛔ У вас нет доступа к этой команде.")
#
# @admin_router.callback_query(F.data.startswith("category_"))
# async def select_category(callback: CallbackQuery, state: FSMContext):
#     category = callback.data  # Получаем выбранную категорию
#     await state.update_data(category=category)  # Сохраняем в контексте
#     await callback.message.answer(f"Вы выбрали категорию: {category}")
#
#     user_data = await state.get_data()
#
#     name = user_data.get('name')
#     url = user_data.get('url')
#     size = user_data.get('size')
#     color = user_data.get('color')
#     description = user_data.get('description')
#     photo = user_data.get('photo')
#     price = user_data.get('price')
#     category = user_data.get('category')
#
#     print(name, url, size, color, description, photo, price, category)
#     await state.clear()


