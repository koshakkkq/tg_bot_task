"""Конвертер валюты"""
import asyncio
import logging

import requests

from create import exchange_token

async def get_exchange_rates_msg(base_currency, convert_currency, value) -> str:
	"""Генерирует сообщение с результатом конвертации"""
	try:
		conversion_rate = await get_exchange_rates(base_currency, convert_currency)
	except Exception as e:
		logging.error(e)
		return 'К сожаление произошла ошибка, вернитесь в меню.'

	converted_value = value * conversion_rate

	try:
		response_msg = '{value} {base_currency} = {converted_value} {convert_currency}'.format(
			value=value,
			base_currency=base_currency,
			converted_value=converted_value,
			convert_currency=convert_currency
		)
	except Exception as e:
		logging.error(e)
		return 'К сожаление произошла ошибка, вернитесь в меню.'

	return response_msg


class BadResponse(Exception):
	"""Исключение для плохого ответа на запрос."""
	pass


async def get_exchange_rates(base_currency, convert_currency) -> float:
	"""Запрос с получением курса валюты base_currency/convert_currency"""
	url = 'https://v6.exchangerate-api.com/v6/{key}/pair/{base_currency}/{convert_currency}'.format(
		key=exchange_token,
		base_currency=base_currency,
		convert_currency=convert_currency,
	)

	loop = asyncio.get_event_loop()
	response_data = await loop.run_in_executor(None, requests.get, url)

	try:
		data = response_data.json()
	except Exception as e:
		raise BadResponse(response_data.content)

	if data['result'] != 'success':
		raise BadResponse(data['error-type'])

	conversion_rate = data['conversion_rate']

	return conversion_rate
