from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from app.states import *
from db.get_data import *
import keyboards.keyboards as kb
from db.update_data import add_review

make_review_router = Router()


@make_review_router.callback_query(F.data == "review_kb")
async def check_review(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите желаемую опцию:", reply_markup=kb.reviews)


def get_review_keyboard(index, total):
    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"prev_review:{index - 1}"))
    buttons.append(InlineKeyboardButton(text=f"{index + 1}/{total}", callback_data="noop"))
    if index < total - 1:
        buttons.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"next_review:{index + 1}"))

    navigation_row = [buttons]
    back_button = [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back_to_menu")]

    return InlineKeyboardMarkup(inline_keyboard=navigation_row + [back_button])


@make_review_router.callback_query(F.data == "check_reviews")
async def check_review(callback: CallbackQuery, state: FSMContext):
    reviews = get_reviews()
    if not reviews:
        await callback.message.answer("Отзывов пока нет.")
        return

    await state.update_data(reviews=reviews, review_index=0)
    await show_review(callback, state, 0)


async def show_review(callback: CallbackQuery, state: FSMContext, index: int):
    data = await state.get_data()
    reviews = data.get("reviews", [])

    if 0 <= index < len(reviews):
        review = reviews[index]
        text = (f"Имя пользователя: {review[0]}\n"
                f"Оценка: {'⭐' * review[1]}\n"
                f"Комментарий: {review[2]}\n"
                f"Дата создания: {review[3]}")
        keyboard = get_review_keyboard(index, len(reviews))
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.update_data(review_index=index)


@make_review_router.callback_query(F.data.startswith("next_review"))
async def next_review(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])
    await show_review(callback, state, index)


@make_review_router.callback_query(F.data.startswith("prev_review"))
async def prev_review(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])
    await show_review(callback, state, index)


@make_review_router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Вы вернулись в меню", reply_markup=kb.reviews)




@make_review_router.callback_query(F.data == "post_review")
async def ask_for_rating(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PostReview.stars)
    await callback.message.answer(
        "Напишите оценку от 1 до 5:"
    )
    await callback.answer()


@make_review_router.message(PostReview.stars)
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


@make_review_router.message(PostReview.comment)
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
                "Спасибо за отзыв!", reply_markup=kb.reviews
            )
        except Exception as e:
            await message.answer("Не удалось добавить отзыв!", reply_markup=kb.reviews)

        await state.clear()
    else:
        await message.answer(
            "Комментарий должен содержать менее 200 символов!"
        )


