import struct

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from poll.keyboards import poll_keyboard
from poll.poll_send import create_dict_from_poll, get_poll_id_msg, get_poll_from_command, delete_poll
from filter import is_chat_non_private
import menu


class PollStates(StatesGroup):
	pending_poll = State()


async def get_picture_msg(message: types.Message, state: FSMContext):
	await state.reset_data()
	await message.answer(text='Воспользуйтесь кнопкой!', reply_markup=poll_keyboard)
	await state.set_state(PollStates.pending_poll.state)


async def create_poll(message: types.Message, state: FSMContext):
	poll = message.poll
	create_dict_from_poll(poll)
	response_msg = await get_poll_id_msg(message.poll, message.message_id, message.chat.id)
	await message.answer(response_msg)
	await menu.menu_msg(message, state)


async def send_poll_to_chat(message: types.Message, state: FSMContext):
	poll_to_send = await get_poll_from_command(message.text)
	if poll_to_send is None:
		return
	await message.answer_poll(**poll_to_send)
	await delete_poll(message.text)


def handler_register(dp: Dispatcher):
	dp.register_message_handler(get_picture_msg, state=menu.MenuStates.in_menu, text='Опрос')
	dp.register_message_handler(create_poll, state=PollStates.pending_poll, content_types=['poll'])
	dp.register_message_handler(send_poll_to_chat, is_chat_non_private, state='*', text_startswith='/poll_')
