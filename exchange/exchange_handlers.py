"""Обработка хэндлеров для обменика валюты"""

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from exchange.get_exchange_rates import get_exchange_rates_msg
import menu
from exchange.keyboards import get_currency_keyboard
import exchange.utils


class ExchangeStates(StatesGroup):
	"""Состояния для обменика валют"""
	currency_pick = State()
	get_base_currency_value = State()
	final = State()


async def exchange_begin_msg(message: types.Message, state: FSMContext):
	"""Срабатывает при переходе из меню, вызывает функцию для показа всех валют c приветственным сообщением."""
	await state.reset_state()
	await currency_selection_msg(message, state, 'Выберите валюту из которой будет произведена конвертация')
	await state.set_state(ExchangeStates.currency_pick.state)


async def currency_selection_msg(message: types.Message, state: FSMContext, response_message):
	"""
	Вызывается при выборе валюты из которой происходит конвертация,
	и при выборе выалюты в которую происходит конвертация, с соответсвующими сообщениями.
	"""
	await state.update_data(page=1)
	keyboard = get_currency_keyboard(1)
	await message.answer(text=response_message, reply_markup=keyboard)


async def currency_selection_next_page(callback: types.CallbackQuery, state: FSMContext):
	"""Получение следующей страницы с валютами."""
	data = await state.get_data()
	page = data['page']
	max_page = exchange.utils.get_max_currency_page()
	if page + 1 > max_page:
		await callback.answer('Вы пользуетесь на актуальной клавиатурой!')
		return
	await state.update_data(page=page + 1)
	await currencies_selection_markup_edit(callback, state)
	await callback.answer()


async def currency_selection_prev_page(callback: types.CallbackQuery, state: FSMContext):
	"""Получение предыдущей страницы с валютами."""
	data = await state.get_data()
	page = data['page']
	if page == 1:
		await callback.answer('Вы пользуетесь на актуальной клавиатурой!')
		return
	await state.update_data(page=page - 1)
	await currencies_selection_markup_edit(callback, state)


async def currencies_selection_markup_edit(callback: types.CallbackQuery, state: FSMContext):
	"""Редактирует клавиатуру в зависимости от выбранной страницы."""
	data = await state.get_data()
	page = data['page']
	keyboard = get_currency_keyboard(page)
	await callback.message.edit_reply_markup(reply_markup=keyboard)


async def pick_currency(callback: types.CallbackQuery, state: FSMContext):
	"""
	Вызывается при выборе валюты, если base_currency(валюту из которой будет произведена конвертация) не выбрана,
	то в машину состояний сохраняется выбраная валюта, иначе сохраняется значение convert_currency и выводится
	сообщение с выбранными валютами, и предложением ввести количество валюты для конвертации.
	"""
	currency_picked = callback.data.split('_')[-1]
	data = await state.get_data()
	if 'base_currency' not in data:
		await state.update_data(base_currency=currency_picked)
		response_message = exchange.utils.get_picked_currency_msg(currency_picked)
		await currency_selection_msg(callback.message, state, response_message)
		await callback.answer()
	else:
		await state.update_data(convert_currency=currency_picked)
		response_message = exchange.utils.get_value_info_msg(
			base_currency=data['base_currency'],
			convert_currency=currency_picked,
		)
		await callback.message.answer(response_message)
		await state.set_state(ExchangeStates.get_base_currency_value.state)


async def get_exchange_value(message: types.Message, state: FSMContext):
	"""
	Получает количество валюты для конвертации проверяет её валидность(float или нет), в случае
	если значение не число, выводит сообщение о том, что значение не корректно, иначе выводит пользователю
	сообщение с результатом конвертации.
	"""
	value = message.text
	value = value.replace(',', '.')
	value = exchange.utils.is_float(value)
	if value == None:
		await message.answer('Вы ввели не число, введите корректное значение ещё раз.')
	else:
		data = await state.get_data()
		response_msg = await get_exchange_rates_msg(
			base_currency=data['base_currency'],
			convert_currency=data['convert_currency'],
			value=value,
		)
		await message.answer(response_msg)


def handler_register(dp: Dispatcher):
	"""Регистрация хэндлеров"""

	dp.register_message_handler(exchange_begin_msg, state=menu.MenuStates.in_menu, text='Конвертер валют')

	dp.register_callback_query_handler(currency_selection_prev_page, state=ExchangeStates.currency_pick, text='prev')
	dp.register_callback_query_handler(currency_selection_next_page, state=ExchangeStates.currency_pick, text='next')

	dp.register_callback_query_handler(
		pick_currency,
		state=ExchangeStates.currency_pick,
		text_startswith='pick_currency_',
	)

	dp.register_message_handler(get_exchange_value, state=ExchangeStates.get_base_currency_value.state)
