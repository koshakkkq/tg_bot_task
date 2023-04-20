from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from pictures.get_random_picture import get_random_picture_msg
import menu

async def get_picture_msg(message: types.Message, state: FSMContext):
	"""Хэндлер для выдачи случайной картинки."""
	await state.reset_data()
	msg = await get_random_picture_msg()
	await message.answer(text=msg, parse_mode="Markdown")
	await menu.menu_msg(message, state)

def handler_register(dp: Dispatcher):
	dp.register_message_handler(get_picture_msg, state=menu.MenuStates.in_menu, text='Картинка')