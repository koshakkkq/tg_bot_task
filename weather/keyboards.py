from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

get_location = [[KeyboardButton(text='Местоположение', request_location=True)],
				[KeyboardButton(text='Главное меню')]]

get_location_keyboard = ReplyKeyboardMarkup(keyboard=get_location, resize_keyboard=True)
