import asyncio

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from weather.get_weather import get_current_weather
import menu
from weather.keyboards import get_location_keyboard
from weather.get_weather import WeatherStatusCode


class WeatherStates(StatesGroup):
	pending_location = State()
	got_temperature = State()


async def get_location_msg(message: types.Message, state: FSMContext):
	"""Хэндлер для калвиатуры с геолокацией"""
	await state.reset_data()
	await message.answer(
		'Для того что бы узнать погоду отправьте ваше местоположение или напишите город.',
		reply_markup=get_location_keyboard,
	)
	await state.set_state(WeatherStates.pending_location.state)


async def get_weather_by_location(message: types.Message, state: FSMContext):
	"""Хэндлер если пользователь отправит местоположение"""
	coords = (message.location.latitude, message.location.longitude)
	status, response_msg = await get_current_weather(coords=coords)
	await get_weather_msg(message, state, status, response_msg)


async def get_weather_by_name(message: types.Message, state: FSMContext):
	"""Хэндлер если пользователь отправит город"""
	city_name = message.text
	status, response_msg = await get_current_weather(city_name=city_name)
	await get_weather_msg(message, state, status, response_msg)


async def get_weather_msg(message: types.Message, state: FSMContext, status, response_msg):
	"""Хэндлер для получение информации о погоде в заданном городе."""
	if WeatherStatusCode.no_city_found == status:
		await message.answer(text=response_msg)
		await asyncio.sleep(0.05)
		await get_location_msg(message, state)

	elif WeatherStatusCode.success == status:
		await message.answer(text=response_msg)
		await state.set_state(WeatherStates.got_temperature.state)

	elif WeatherStatusCode.err == status:
		await message.answer(text=response_msg)
		await asyncio.sleep(0.05)
		await get_location_msg(message, state)


def handler_register(dp: Dispatcher):
	dp.register_message_handler(get_location_msg, state=menu.MenuStates.in_menu, text='Погода')

	dp.register_message_handler(
		get_weather_by_location,
		state=WeatherStates.pending_location,
		content_types=['location']
	)

	dp.register_message_handler(get_weather_by_name,state=WeatherStates.pending_location)

	dp.register_message_handler(get_location_msg,state=WeatherStates.pending_location)
