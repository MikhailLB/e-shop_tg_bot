from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from db.delete_data import remove_from_cart
from db.update_data import *
from db.get_data import *
from app.states import *
import keyboards.keyboards as kb

from parse import parse_obj, photo_parse

router = Router()
class CartCallback(CallbackData, prefix="cart"):
    action: str
    item_id: int

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\n"
                        f"Выбери нужную опцию!"
                        , reply_markup=kb.main_keyboard)
    user_id = message.from_user.id
    add_user(user_id)

@router.message(F.text == "Назад")
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы вернулись назад", reply_markup=kb.main_keyboard)

@router.message(F.text == "Оформление заказа")
async def make_order(message: Message):
    await message.answer("Выберите опцию:", reply_markup=kb.make_order_keyboard)

@router.message(F.text == "Найти товар")
async def find_item(message: Message, state: FSMContext):
    await state.set_state(MakeOrder.link)
    await message.answer("Укажите ссылку на товар\nПример: https://www.poizon.com/product/jordan-1-low-ashen-slate-men-s-53540881?track_referer_page_id=2296&track_referer_block_type=4766&track_referer_position=3\n")

@router.message(MakeOrder.link)
async def add_to_cart(message: Message, state: FSMContext):
    await state.set_state(MakeOrder.link)

    if 'https://www.poizon.com' in message.text:
        await state.update_data(link=message.text)
        await state.update_data(user_id=message.from_user.id)

        add_to_cart_button = InlineKeyboardButton(text="Добавить в корзину", callback_data="add_to_cart")

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[add_to_cart_button]])
        try:
            await message.answer("Идет поиск товара...")
            price_name = parse_obj(message.text)
            photo = photo_parse(message.text).split('?')[0]
            await state.update_data(price=price_name[0])
            await state.update_data(name=price_name[1])

            if price_name:
                await message.answer_photo(photo=photo, caption=f"Название товара: {price_name[1]}\n\nЦена:{price_name[0]}", reply_markup=keyboard)
            else:
                await message.answer("Товар не найден!")
        except Exception as e:
            await message.answer("Товар не найден!")

    else:
        await message.answer("Не правильный формат ссылки!\nСсылка должна начинаться на: https://www.poizon.com")


@router.callback_query(lambda c: c.data == 'add_to_cart')
async def add_to_cart(callback_query: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    link = user_data.get('link')
    user_id = user_data.get('user_id')
    price = user_data.get('price').replace("$", "")
    name = user_data.get('name')
    print(price, name)
    if link:
        try:
            add_to_cart_db(user_id, link, price, name)
            await callback_query.answer("Товар добавлен в корзину.")
            await callback_query.message.answer(f"Товар {name} был добавлен в вашу корзину.",
                                                reply_markup=kb.main_keyboard)
        except Exception as e:
            await callback_query.answer("Не удалось добавить товар в корзину")

        await state.clear()
    else:
        await callback_query.answer("Ошибка. Ссылка на товар не найдена.")


@router.message(F.text == "Корзина")
async def cart(message: Message):
    try:
        user_id = message.from_user.id
        goods = get_cart_items(user_id)

        if not goods:
            await message.answer("Ваша корзина пуста.")
            return

        await message.answer(f"В вашей корзине {len(goods)} товаров:")

        for good in goods:
            price, name, thing_link = good
            item_id = find_id(user_id, thing_link)
            remove_to_cart_button = InlineKeyboardButton(
                text="Удалить из корзины",
                callback_data=CartCallback(action="delete", item_id=item_id[0]).pack()
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[remove_to_cart_button]])
            await message.answer(f"Товар: {name}\nЦена: {price}$\nСсылка: {thing_link}", reply_markup=keyboard)
    except Exception as e:
        print(e)
        await message.answer("Не удалось посмотреть корзину, попробуйте еще раз!")



@router.callback_query()
async def delete_from_cart(callback_query: CallbackQuery):
    callback_data = CartCallback.unpack(callback_query.data)
    if callback_data.action == "delete":
        user_id = callback_query.from_user.id
        item_id = callback_data.item_id
        try:
            remove_from_cart(user_id, item_id)
            await callback_query.message.edit_text(f"Товар успешно удален из корзины!")
        except Exception as e:
            print(e)
            await callback_query.answer("Не удалось удалить товар из корзины, попробуйте еще раз!")
        await callback_query.answer()



@router.message(F.text == "Оформить заказ")
async def personal_data(message: Message, state: FSMContext):
    user_already_register = False
    info = get_info_for_account_check(message.from_user.id)

    if any(i != "None" for i in info):
        user_already_register = True

    if not user_already_register:
        await state.set_state(Reg.name)
        await message.answer(
            "Для оформления заказа вам нужно указать:\n"
            "Имя\n"
            "Фамилию\n"
            "Адрес ближайшего постамата (город, улица, район, индекс)\n"
            "Давайте начнем! (Информацию можно будет отредактировать в профиле)"
        )
        await message.answer("Введите ваше имя:")
    else:
        await message.answer(
            "Вы уже зарегистрированы. Желаете изменить информацию?", reply_markup=kb.edit_personal_data_information
        )

@router.message(F.text == "Изменить адрес доставки")
async def personal_data(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer(
        "Для изменения данных укажите:\n"
        "Имя\n"
        "Фамилию\n"
        "Адрес ближайшего постамата (город, улица, район, индекс)\n"
        "Давайте начнем! (Информацию можно будет отредактировать в профиле)", reply_markup=kb.come_back
    )
    await message.answer("Введите ваше имя:")

@router.message(Reg.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.second_name)
    await message.answer("Введите вашу фамилию:")


@router.message(Reg.second_name)
async def get_second_name(message: Message, state: FSMContext):
    await state.update_data(second_name=message.text)
    await state.set_state(Reg.city)
    await message.answer("В каком городе вы живете?")


@router.message(Reg.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("На какой улице?")
    await state.set_state(Reg.street)


@router.message(Reg.street)
async def get_street(message: Message, state: FSMContext):
    await state.update_data(street=message.text)
    await message.answer("В каком районе?")
    await state.set_state(Reg.district)


@router.message(Reg.district)
async def get_district(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await message.answer("Ваш индекс:")
    await state.set_state(Reg.index)

@router.message(Reg.index)
async def get_index(message: Message, state: FSMContext):
    await state.update_data(index=message.text)

    user_id = message.from_user.id
    user_data = await state.get_data()
    name = user_data.get('name')
    second_name = user_data.get('second_name')
    city = user_data.get('city')
    street = user_data.get('street')
    district = user_data.get('district')
    index = user_data.get('index')

    try:
        update_user_data(user_id, name, second_name, city, street, district, index)
        await message.answer(f"Спасибо за информацию!\n"
                             f"Имя: {name}\n"
                             f"Фамилия: {second_name}\n"
                             f"Город: {city}\n"
                             f"Улица: {street}\n"
                             f"Район: {district}\n"
                             f"Почтовый индекс: {index}")
    except Exception as e:
        await message.answer(f"Ошибка при создании пользователя! Попробуйте еще раз")

    await state.clear()

@router.message(F.text == "Отзывы")
async def reviews(message: Message):
    await message.answer(
        "Выберите желаемую опцию:", reply_markup=kb.reviews
    )

@router.message(F.text == "Посмотреть отзывы")
async def check_review(message: Message):

    await message.answer(
        "Отзывы:", reply_markup=kb.come_back
    )
    try:
        reviews = get_reviews(10)
        if reviews:
            for review in reviews:
                await message.answer(f"Имя пользователя: {review[0]}\n"
                                     f"Оценка: {'⭐' * review[1]}\n"
                                     f"Комментарий: {review[2]}\n"
                                     f"Дата создания: {review[3]}")
    except Exception as e:
        await message.answer("Не удалось получить отзывы")

@router.message(F.text == "Оставить отзыв")
async def ask_for_rating(message: Message, state: FSMContext):
    await state.set_state(PostReview.stars)
    await message.answer(
        "Напишите оценку от 1 до 5:"
    )


@router.message(PostReview.stars)
async def process_rating(message: Message, state: FSMContext):
    if message.text in ['1', '2', '3', '4', '5']:
        await state.update_data(stars=message.text)
        await state.set_state(PostReview.comment)
        await message.answer(
            "Напишите комментарий до 200 символов, если хотите оставить оценку без комментария, напишите прочерк (-)"
        )
    else:
        await message.answer(
            "Неверный формат, просто введите число от 1 до 5"
        )


@router.message(PostReview.comment)
async def process_comment(message: Message, state: FSMContext):
    if len(message.text) <= 200 or message.text == "-":
        await state.update_data(comment=message.text)
        data = await state.get_data()

        user_id = message.from_user.id
        rating = data['stars']
        comment = data['comment']
        user_name = message.from_user.username

        try:

            add_review(user_id, rating, comment, user_name)
            await message.answer(
                "Спасибо за отзыв!", reply_markup=kb.main_keyboard
            )
        except Exception as e:
            await message.answer("Не удалось добавить отзыв!", reply_markup=kb.main_keyboard)

        await state.clear()
    else:
        await message.answer(
            "Комментарий должен содержать менее 200 символов!"
        )
