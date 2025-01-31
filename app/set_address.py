from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states import *
from db.get_data import *
import keyboards.keyboards as kb
from db.update_data import update_user_data, delete_user_data

set_order_router = Router()

@set_order_router.callback_query(F.data.startswith("checkout_order"))
async def chose_delivery_method(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите метод доставки: ", reply_markup=kb.choose_delivery_method)
    await callback.answer()

@set_order_router.message(F.text == "Изменить адрес доставки")
async def chose_delivery_method(message: Message, state: FSMContext):
    await message.answer("Выберите метод доставки: ", reply_markup=kb.choose_delivery_method)

@set_order_router.callback_query(F.data.startswith("currier_delivery"))
async def chose_delivery_method3(callback: CallbackQuery, state: FSMContext):
    user_already_register = False
    info = get_info_for_account_check(callback.from_user.id)
    await callback.answer()
    if any(i != "None" for i in info):
        user_already_register = True

    if not user_already_register:
        await state.set_state(RegCurr.delivery_method)
        await state.update_data(delivery_method="Курьер")
        await state.set_state(RegCurr.name)
        await callback.message.answer(
            "Для оформления заказа вам нужно указать:\n"
            "Имя\n"
            "Фамилию\n"
            "Адрес (город, улица, район, индекс)\n"
            "Номер телефона\n"
            "Давайте начнем! (Информацию можно будет отредактировать в профиле)"
        )
        await callback.message.answer("Введите ваше имя:")
    else:
        await callback.message.answer(
            "Вы уже зарегистрированы. Желаете изменить информацию?", reply_markup=kb.edit_personal_data_information
        )

@set_order_router.callback_query(F.data.startswith("change_address"))
async def personal_data(callback: CallbackQuery, state: FSMContext):
    delete_user_data(callback.from_user.id)
    await callback.message.answer("Выберите метод доставки: ", reply_markup=kb.choose_delivery_method)
    await callback.answer()


@set_order_router.message(RegCurr.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegCurr.second_name)
    await message.answer("Введите вашу фамилию:")


@set_order_router.message(RegCurr.second_name)
async def get_second_name(message: Message, state: FSMContext):
    await state.update_data(second_name=message.text)
    await state.set_state(RegCurr.city)
    await message.answer("В каком городе вы живете?")


@set_order_router.message(RegCurr.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Укажите на какой улице вы живете (С домом и квартирой, пример: Улица Пушкина 7 кв. 23)")
    await state.set_state(RegCurr.street)


@set_order_router.message(RegCurr.street)
async def get_street(message: Message, state: FSMContext):
    await state.update_data(street=message.text)
    await message.answer("В каком районе?")
    await state.set_state(RegCurr.district)


@set_order_router.message(RegCurr.district)
async def get_district(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await message.answer("Ваш индекс:")
    await state.set_state(RegCurr.index)

@set_order_router.message(RegCurr.index)
async def get_index(message: Message, state: FSMContext):
    await state.update_data(index=message.text)
    await message.answer("Ваш номер телефона:")
    await state.set_state(RegCurr.telephone)

@set_order_router.message(RegCurr.telephone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(telephone=message.text)

    user_id = message.from_user.id
    user_data = await state.get_data()
    name = user_data.get('name')
    second_name = user_data.get('second_name')
    city = user_data.get('city')
    street = user_data.get('street')
    district = user_data.get('district')
    index = user_data.get('index')
    telephone = user_data.get('telephone')
    delivery_method = user_data.get('delivery_method')

    try:
        update_user_data(user_id, name, second_name, city, street, district, index, telephone, delivery_method)
        await message.answer(f"Спасибо за информацию!\n"
                             f"Имя: {name}\n"
                             f"Фамилия: {second_name}\n"
                             f"Город: {city}\n"
                             f"Улица: {street}\n"
                             f"Район: {district}\n"
                             f"Почтовый индекс: {index}\n"
                             f"Телефон: {telephone}\n"
                             f"Метод доставки: {delivery_method}", reply_markup=kb.make_order_continue_keyboard)

        await message.answer(f"Выбери нужную опцию, {message.from_user.first_name}!\n")
    except Exception as e:
        await message.answer(f"Ошибка при создании пользователя! Попробуйте еще раз")

    await state.clear()

@set_order_router.callback_query(F.data.startswith("postomat_delivery"))
async def chose_delivery_method3(callback: CallbackQuery, state: FSMContext):
    user_already_register = False
    info = get_info_for_account_check(callback.from_user.id)
    await callback.answer()
    if any(i != "None" for i in info):
        user_already_register = True

    if not user_already_register:
        await state.set_state(RegPost.delivery_method)
        await state.update_data(delivery_method="Постомат")
        await state.set_state(RegPost.name)
        await callback.message.answer(
            "Для оформления заказа вам нужно указать:\n"
            "Имя\n"
            "Фамилию\n"
            "Адрес ближайшего постомата\n"
            "Телефон\n"
            "Давайте начнем! (Информацию можно будет отредактировать в профиле)"
        )
        await callback.message.answer("Введите ваше имя:")
    else:
        await callback.message.answer(
            "Вы уже зарегистрированы. Желаете изменить информацию?", reply_markup=kb.edit_personal_data_information
        )

@set_order_router.message(RegPost.name)
async def get_name_post(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RegPost.second_name)
    await message.answer("Введите вашу фамилию:")


@set_order_router.message(RegPost.second_name)
async def get_second_name_post(message: Message, state: FSMContext):
    await state.update_data(second_name=message.text)
    await state.set_state(RegPost.city)
    await message.answer("В каком городе вы живете?")


@set_order_router.message(RegPost.city)
async def get_city_post(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Укажите адрес ближайшего постомата с его номером:")
    await state.set_state(RegPost.street)


@set_order_router.message(RegPost.street)
async def get_street_post(message: Message, state: FSMContext):
    await state.update_data(street=message.text)
    await message.answer("В каком районе?")
    await state.set_state(RegPost.district)


@set_order_router.message(RegPost.district)
async def get_district_post(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await message.answer("Ваш индекс:")
    await state.set_state(RegPost.index)

@set_order_router.message(RegPost.index)
async def get_index_post(message: Message, state: FSMContext):
    await state.update_data(index=message.text)
    await message.answer("Ваш номер телефона:")
    await state.set_state(RegPost.telephone)

@set_order_router.message(RegPost.telephone)
async def get_phone_post(message: Message, state: FSMContext):
    await state.update_data(telephone=message.text)
    user_id = message.from_user.id
    user_data = await state.get_data()
    name = user_data.get('name')
    second_name = user_data.get('second_name')
    city = user_data.get('city')
    street = user_data.get('street')
    district = user_data.get('district')
    index = user_data.get('index')
    telephone = user_data.get('telephone')
    delivery_method = user_data.get('delivery_method')

    try:
        update_user_data(user_id, name, second_name, city, street, district, index, telephone, delivery_method)
        await message.answer(f"Спасибо за информацию!\n"
                             f"Имя: {name}\n"
                             f"Фамилия: {second_name}\n"
                             f"Город: {city}\n"
                             f"Улица: {street}\n"
                             f"Район: {district}\n"
                             f"Почтовый индекс: {index}\n"
                             f"Телефон: {telephone}\n"
                            f"Метод доставки: {delivery_method}", reply_markup=kb.make_order_continue_keyboard)
    except Exception as e:
        await message.answer(f"Ошибка при создании пользователя! Попробуйте еще раз")

    await state.clear()