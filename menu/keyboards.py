"""Клавиатура для меню."""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_buttons = [
	[KeyboardButton(text='Погода')],
	[KeyboardButton(text='Конвертер валют')],
	[KeyboardButton(text='Картинка')],
	[KeyboardButton(text='Опрос')],
]

menu_keyboards = ReplyKeyboardMarkup(keyboard=menu_buttons, resize_keyboard=True)