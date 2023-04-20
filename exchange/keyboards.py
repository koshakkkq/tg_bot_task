"""Клавиатры для модуля exchange"""

from create import available_currencies
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

currency_on_page_cnt = 15


def get_currency_keyboard(page):
	"""
	Возвращает клавиатуру с валютами для заданной страницы.
	"""
	start = (page - 1) * currency_on_page_cnt
	end = min(
		page * currency_on_page_cnt,
		len(available_currencies),
	)

	currency_on_page = available_currencies[start:end]

	currency_buttons = []

	for i in range(0, len(currency_on_page), 3):
		buttons_row = []
		for j in range(i, min(i + 3, len(currency_on_page))):
			callback_data = 'pick_currency_{code}'.format(code=currency_on_page[j])
			buttons_row.append(InlineKeyboardButton(text=currency_on_page[j], callback_data=callback_data))
		currency_buttons.append(buttons_row)
	#Провека чтобы на первой странице не было кнопки назад, а на последней вперёд.
	if page * currency_on_page_cnt >= len(available_currencies):
		currency_buttons.append([
			InlineKeyboardButton(text='⬅', callback_data='prev'),
		])
	elif page == 1:
		currency_buttons.append([
			InlineKeyboardButton(text='➡', callback_data='next')
		])
	else:
		currency_buttons.append([
			InlineKeyboardButton(text='⬅', callback_data='prev'),
			InlineKeyboardButton(text='➡', callback_data='next')
		])

	return InlineKeyboardMarkup(inline_keyboard=currency_buttons)
