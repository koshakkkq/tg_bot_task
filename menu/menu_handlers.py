"""Обработка хэндлеров для главного меню"""

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from menu.keyboards import menu_keyboards
from menu.messages import get_menu_msg
from filter import is_chat_private

class MenuStates(StatesGroup):
	"""Состояние того, что пользоватль в меню"""
	in_menu = State()


async def menu_msg(message: types.Message, state: FSMContext):
	"""Хэндлер для меню."""
	await state.reset_data()
	res_message = get_menu_msg(message.chat.first_name)
	await message.answer(text=res_message, reply_markup=menu_keyboards)
	await state.set_state(MenuStates.in_menu.state)


def handler_register(dp: Dispatcher):
	"""Регистрация хэндлеров"""
	dp.register_message_handler(menu_msg, is_chat_private ,state="*", commands=['start','menu'])
