from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.admin_states import GetId
from app.states import AddDeliveryLink, DeleteProduct
from keyboards.admin_keyboards import *
import openpyxl
from aiogram import types
from aiogram.filters import Command
from db.update_data import insert_products, add_order_status, add_order_delivery_link, delete_product_by_name, \
    add_admin_to_db, delete_admin_from_bd
from db.get_data import *


admin_router = Router()

def admins_users():
    ADMINS = fetch_admins()
    return ADMINS

def admins_users_name():
    ADMINS = admins_name()
    return ADMINS


def get_order_statuses_keyboard(order_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В обработке", callback_data=f"order_in_process:{order_id}")],
        [InlineKeyboardButton(text="В процессе оформления", callback_data=f"order_accepted:{order_id}")],
        [InlineKeyboardButton(text="Отправлен", callback_data=f"order_sent:{order_id}")],
        [InlineKeyboardButton(text="Выполнен", callback_data=f"order_complete:{order_id}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"now_orders_kb")]
    ])

def create_order_navigation_kb(order_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить статус заказа", callback_data=f"change_order_status:{order_id}"),
            InlineKeyboardButton(text="Изменить ссылку на отслеживание", callback_data=f"change_tracking_link:{order_id}")
        ],
        [InlineKeyboardButton(text="Назад", callback_data="get_back")]
    ])
    return keyboard

@admin_router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in admins_users().keys():
        await state.clear()
        await message.answer("🔹 Добро пожаловать в панель администратора!", reply_markup=admin_keyboard)
    else:
        await message.answer("⛔ У вас нет доступа к этой команде.")

@admin_router.callback_query(F.data == "product_control")
async def product_control(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id in admins_users().keys():
        await callback.message.edit_text("🔹 Управление товарами", reply_markup=goods)
    else:
        await callback.message.edit_text("⛔ У вас нет доступа к этой команде.")

@admin_router.callback_query(F.data == "get_back")
async def back_to_admin_menu(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    if user_id in admins_users().keys():
        await state.clear()
        await callback.message.edit_text("🔹 Добро пожаловать в панель администратора!", reply_markup=admin_keyboard)
    else:
        await callback.message.edit_text("⛔ У вас нет доступа к этой команде.")

@admin_router.callback_query(F.data == "delete_product")
async def delete_product(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if user_id in admins_users().keys():
        await callback.message.edit_text("Укажите имя товара или ссылку на товар: ", reply_markup=get_admin_back_to_mainmenu)
        await state.set_state(DeleteProduct.name)
    else:
        await callback.message.edit_text("⛔ У вас нет доступа к этой команде.")

@admin_router.message(DeleteProduct.name)
async def find_del_pr(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in admins_users().keys():
        await state.update_data(name=message.text)
        data = await state.get_data()
        name = data.get('name')
        try:
            delete_product_by_name(name)
            await message.answer(f"Товар {name} успешно удален!", reply_markup=goods)
            await state.clear()
        except Exception as e:
            await message.answer(f"Ошибка! Товар {name} не найден!", reply_markup=goods)
    else:
        await message.edit_text("⛔ У вас нет доступа к этой команде.")

@admin_router.callback_query(F.data == "add_product")
async def start_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in admins_users().keys():
        await callback.message.edit_text("Отправьте Excel файл со следующими колонками: name, url, size, color, description, photo_url, price, category", reply_markup=get_admin_back_to_mainmenu)
    else:
        await callback.message.edit_text("⛔ У вас нет доступа к этой команде.")

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
            await message.answer("Ошибка: В файле отсутствуют необходимые колонки!", reply_markup=get_admin_back_to_mainmenu)
            return

        data_list = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data_list.append(list(row))

        insert_products(data_list)
        await message.answer(f"Товары добавлены в БД", reply_markup=admin_keyboard)

    except Exception as e:
        await message.answer(f"Ошибка при обработке файла: {e}", reply_markup=get_admin_back_to_mainmenu)


@admin_router.callback_query(F.data == "order_control")
async def products_controller(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in admins_users().keys():
        await callback.message.edit_text("Выберите опцию:", reply_markup=orders_keyboard)
    else:
        await callback.message.edit_text("⛔ У вас нет доступа к этой команде.")


@admin_router.callback_query(F.data == "now_orders_kb")
async def show_orders_admin(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in admins_users().keys():
        await callback.answer("⛔ У вас нет доступа к этой команде.")
        return

    orders = get_orders_for_admin()
    if not orders:
        await callback.message.edit_text("Нет текущих заказов.", reply_markup=get_admin_back_to_mainmenu)
        return
    await show_order(callback, orders, index=0)

async def show_order(callback: CallbackQuery, orders, index: int):
    order = orders[index]
    order_id, name, price, delivery_method, size, color, address, status, tracking_link = order

    text = (
        f"📦 **Заказ #{order_id}**\n"
        f"Название: {name}\n"
        f"Цена: {price}₽\n"
        f"Доставка: {delivery_method}\n"
        f"Размер: {size}\n"
        f"Цвет: {color}\n"
        f"Адрес: {address}\n"
        f"Статус: {status}\n"
        f"Ссылка для отслеживания: {tracking_link or 'Отсутствует'}\n"
    )

    navigation_kb = InlineKeyboardBuilder()
    if index > 0:
        navigation_kb.button(text="⬅️ Предыдущий", callback_data=f"prev_order_admin:{index-1}")
    if index < len(orders) - 1:
        navigation_kb.button(text="Следующий ➡️", callback_data=f"next_order_admin:{index+1}")

    keyboard = create_order_navigation_kb(order_id)
    keyboard.inline_keyboard += navigation_kb.as_markup().inline_keyboard

    await callback.message.edit_text(text, reply_markup=keyboard)

@admin_router.callback_query(F.data.startswith("next_order_admin"))
async def next_order_admin(callback: CallbackQuery):
    index = int(callback.data.split(":")[1])
    orders = get_orders_for_admin()
    await show_order(callback, orders, index)

@admin_router.callback_query(F.data.startswith("prev_order_admin"))
async def prev_order_admin(callback: CallbackQuery):
    index = int(callback.data.split(":")[1])
    orders = get_orders_for_admin()
    await show_order(callback, orders, index)

@admin_router.callback_query(F.data == "fulfill_orders")
async def show_fulfill_orders_admin(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in admins_users():
        await callback.answer("⛔ У вас нет доступа к этой команде.")
        return

    orders = get_all_orders_for_admin()
    if not orders:
        await callback.message.edit_text("Нет заказов!", reply_markup=get_admin_back_to_mainmenu)
        return

    await show_order(callback, orders, index=0)

@admin_router.callback_query(F.data.startswith("change_order_status"))
async def change_order_status(callback: CallbackQuery):
    order_id = callback.data.split(":")[1]
    await callback.message.edit_text(
        f"Изменение статуса для заказа #{order_id}, выберите статус:",
        reply_markup=get_order_statuses_keyboard(order_id)
    )

@admin_router.callback_query(F.data.startswith("order_in_process"))
async def change_order_status_in_process(callback: CallbackQuery):
    order_id = callback.data.split(":")[1]
    add_order_status(order_id, "В обработке")
    await callback.message.edit_text(f"Статус изменен на 'В обработке'", reply_markup=orders_keyboard)

@admin_router.callback_query(F.data.startswith("order_accepted"))
async def change_order_status_order_accepted(callback: CallbackQuery):
    order_id = callback.data.split(":")[1]
    add_order_status(order_id, "В процессе оформления")
    await callback.message.edit_text(f"Статус изменен на 'В процессе оформления!'", reply_markup=orders_keyboard)

@admin_router.callback_query(F.data.startswith("order_sent"))
async def change_order_status_order_sent(callback: CallbackQuery):
    order_id = callback.data.split(":")[1]
    add_order_status(order_id, "Отправлен")
    await callback.message.edit_text(f"Статус изменен на 'Отправлен'", reply_markup=orders_keyboard)

@admin_router.callback_query(F.data.startswith("order_complete"))
async def change_order_status_order_complete(callback: CallbackQuery):
    order_id = callback.data.split(":")[1]
    add_order_status(order_id, "Заказ выполнен")
    await callback.message.edit_text(f"Статус изменен на 'Заказ выполнен'", reply_markup=orders_keyboard)

@admin_router.callback_query(F.data.startswith("change_tracking_link"))
async def change_tracking_link(callback: CallbackQuery, state: FSMContext):
    order_id = callback.data.split(":")[1]
    await callback.message.edit_text(f"Отправьте ссылку на отслеживание для заказа #{order_id}: ")
    await state.set_state(AddDeliveryLink.link)
    await state.update_data(order_id=order_id)

@admin_router.message(AddDeliveryLink.link)
async def change_tracking_link1(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    data = await state.get_data()
    link = data.get('link')
    order_id = data.get('order_id')
    add_order_delivery_link(order_id, link)
    await message.answer(f"Ссылка для заказа #{order_id} изменена на {link}", reply_markup=orders_keyboard)
    await state.clear()


@admin_router.callback_query(F.data.startswith("admin_control"))
async def admin_control(callback: CallbackQuery):
    user_id = callback.from_user.id
    if admins_users()[user_id] == "super_admin":
        await callback.message.edit_text(f"Выберите действие: ", reply_markup=admin_control_kb)
    else:
        await callback.message.edit_text(f"У вас нет прав на использование этой команды!", reply_markup=get_admin_back_to_mainmenu)


@admin_router.callback_query(F.data.startswith("add_admin"))
async def add_admin(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if admins_users()[user_id] == "super_admin":
        await callback.message.edit_text(f"Чтобы добавить администратора, отправьте его id, пример: 1272027591. Айди можно узнать в боте @getmyid_bot",  reply_markup=get_admin_back_to_mainmenu)
        await state.set_state(GetId.id)
    else:
        await callback.message.edit_text(f"У вас нет прав на использование этой команды!", reply_markup=get_admin_back_to_mainmenu)

@admin_router.message(GetId.id)
async def add_admin2(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    user_id = message.from_user.id
    if admins_users()[user_id] == "super_admin":
        await message.answer(f"Напишите имя нового администратора:",  reply_markup=get_admin_back_to_mainmenu)
        await state.set_state(GetId.name)
    else:
        await message.answer(f"У вас нет прав на использование этой команды!", reply_markup=get_admin_back_to_mainmenu)

@admin_router.message(GetId.name)
async def add_admin1(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if admins_users()[user_id] == "super_admin":
        await state.update_data(name=message.text)
        data = await state.get_data()
        id = data.get('id')
        name = data.get('name')
        try:
            add_admin_to_db(id, name)
            await message.answer(f"Администратор добавлен!", reply_markup=get_admin_back_to_mainmenu)
            await state.clear()

        except Exception as e:
            await message.answer(f"Произошла ошибка!", reply_markup=get_admin_back_to_mainmenu)
            await state.clear()
    else:
        await message.edit_text(f"У вас нет прав на использование этой команды!", reply_markup=get_admin_back_to_mainmenu)


def get_admins_keyboard():
    admins = admins_users_name()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{admin_id}:{admin_name}", callback_data=f"confirm_delete:{admin_id}")]
            for admin_id,admin_name in admins.items()
        ]
    )
    back_button = InlineKeyboardButton(text="Назад", callback_data="get_back")

    keyboard.inline_keyboard += [[back_button]]
    return keyboard


@admin_router.callback_query(F.data.startswith("delete_admin"))
async def delete_admin(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if fetch_admins().get(user_id) == "super_admin":
        await callback.message.edit_text(
            "Выберите администратора, которого хотите удалить:",
            reply_markup=get_admins_keyboard()
        )
    else:
        await callback.message.edit_text(
            "У вас нет прав на использование этой команды!", reply_markup=get_admin_back_to_mainmenu
        )


@admin_router.callback_query(F.data.startswith("confirm_delete:"))
async def confirm_delete_admin(callback: CallbackQuery):
    admin_id = int(callback.data.split(":")[1])
    delete_admin_from_bd(admin_id)
    await callback.message.edit_text(f"Администратор с ID {admin_id} удалён.", reply_markup=get_admin_back_to_mainmenu)


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


