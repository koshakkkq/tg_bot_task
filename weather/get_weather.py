"""Получение температуры"""

import logging

import requests
import asyncio

from create import weather_token

from typing import Tuple

#Коды ошибоки
class WeatherStatusCode(object):
	err = 0
	no_city_found = 1
	success = 2


class BadResponse(Exception):
	pass


err_response_message = 'Ошибка на сервере. Попробуйте ещё раз.'


async def get_current_weather(coords: Tuple[float, float] = (None, None), city_name: str = None) -> (int, str):
	"""
	Возвращает код ошибки, сообщение с температурой в заданной местности, если city_name указан,
	то будет выполенен поиск по городу.
	"""
	if city_name != None:
		try:
			city_found, coords = await get_coords_by_city_name(city_name)
			if city_found == False:
				return WeatherStatusCode.no_city_found, 'Заданного города не найдено!\n Попробуйте ещё раз.'
		except Exception as e:
			logging.error(e)
			return WeatherStatusCode.err, err_response_message

	try:
		cur_temp = await get_temperature_by_coords(coords)
	except Exception as e:
		logging.error(e)
		return WeatherStatusCode.err, err_response_message
	res_msg = 'Сейчас в заданном городе {state},\nтемпература: {temp}, но чувствуется, как {temp_feels_like}'.format(
		state=cur_temp['state'],
		temp=cur_temp['temp'],
		temp_feels_like=cur_temp['temp_feels_like'],
	)
	return WeatherStatusCode.success, res_msg


async def get_temperature_by_coords(coords: Tuple[float, float]):
	"""Получение температуры по заданным координатам"""
	url = 'https://api.openweathermap.org/data/2.5/weather'
	params = {
		'lat': coords[0],
		'lon': coords[1],
		'appid': weather_token,
		'units': 'metric',
		'lang': 'ru',
	}
	loop = asyncio.get_event_loop()

	response = await loop.run_in_executor(None, requests.get, url, params)

	if response.status_code != 200:
		raise BadResponse(response.content)

	response_data = response.json()

	weather_data = {
		'state': response_data['weather'][0]['description'],
		'temp': response_data['main']['temp'],
		'temp_feels_like': response_data['main']['feels_like']
	}
	return weather_data


async def get_coords_by_city_name(city_name) -> (bool, (float, float)):
	"""Получение координат, вернёт найден ли город, и координаты найденого города"""
	url = 'http://api.openweathermap.org/geo/1.0/direct'

	params = {
		'q': city_name,
		'limit': 1,
		'appid': weather_token,
	}
	loop = asyncio.get_event_loop()

	response = await loop.run_in_executor(None, requests.get, url, params)

	if response.status_code != 200:
		raise BadResponse(response.content)

	response_data = response.json()
	if len(response_data) == 0:
		return False, (0, 0)
	lat = response_data[0]['lat']
	lon = response_data[0]['lon']
	return True, (lat, lon)
