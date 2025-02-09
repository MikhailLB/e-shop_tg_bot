from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import back_menu
from db.get_data import *

faq_router = Router()


def get_faq_keyboard(index, total):
    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"prev_faq:{index - 1}"))
    buttons.append(InlineKeyboardButton(text=f"{index + 1}/{total}", callback_data="noop"))
    if index < total - 1:
        buttons.append(InlineKeyboardButton(text="Вперёд ➡️", callback_data=f"next_faq:{index + 1}"))

    navigation_row = [buttons]
    back_button = [InlineKeyboardButton(text="🔙 Вернуться в меню", callback_data="back_to_main_menu")]

    return InlineKeyboardMarkup(inline_keyboard=navigation_row + [back_button])


@faq_router.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery, state: FSMContext):
    faqs = get_faq()
    if not faqs:
        await callback.message.answer("FAQ пока нет.")
        return

    await state.update_data(faqs=faqs, faq_index=0)
    await display_faq(callback, state, 0)


async def display_faq(callback: CallbackQuery, state: FSMContext, index: int):
    data = await state.get_data()
    faqs = data.get("faqs", [])

    if 0 <= index < len(faqs):
        faq = faqs[index]
        text = f"❓ {faq[0]}\n\n💬 {faq[1]}"
        keyboard = get_faq_keyboard(index, len(faqs))
        await callback.message.edit_text(text, reply_markup=keyboard)
        await state.update_data(faq_index=index)


@faq_router.callback_query(F.data.startswith("next_faq"))
async def next_faq(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])
    await display_faq(callback, state, index)


@faq_router.callback_query(F.data.startswith("prev_faq"))
async def prev_faq(callback: CallbackQuery, state: FSMContext):
    index = int(callback.data.split(":")[1])
    await display_faq(callback, state, index)

@faq_router.callback_query(F.data == ("call_support"))
async def prev_faq(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Напишите @m_loboda в личные сообщения о своей проблеме!", reply_markup=back_menu)
