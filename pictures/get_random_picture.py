import asyncio
import logging
import random

import requests

from create import picture_token


async def get_random_picture_msg():
	"""
	Получение сообщения с рандомной кратинкой,
	Вставляет картинку в Markdown, чтобы не нагружать загрузкой картинки.
	"""
	try:
		picture_url = await get_random_picture()
	except Exception as e:
		logging.error(e)
		return 'Ошибка на сервере!'

	try:
		response_msg = '[ ]({url})Картинка милого животного'.format(url=picture_url)
	except Exception as e:
		logging.error(e)
		return 'Ошибка на сервере!'

	return response_msg


class BadResponse(Exception):
	pass


async def get_random_picture():
	"""
	Получает случайную картинку(из 100 рандомных по выдаче в google_images).
	Так как точно не известно кол-во страниц, а serpapi бесплатно, даёт сделать лишь 100 запросов в месяц
	не стал делать рандомизацию по страницам(на одной странице 100 рандомных картинко"
	"""
	url = 'https://serpapi.com/search'

	params = {
		'engine': 'google_images',
		'ijn': 0,
		'api_key': picture_token,
		'q': 'Милые животные',
	}

	loop = asyncio.get_event_loop()
	response = await loop.run_in_executor(None, requests.get, url, params)

	if response.status_code != 200:
		raise BadResponse(response.content)

	response_data = response.json()

	images = response_data['images_results']

	random_image = random.choice(images)
	return random_image['original']
