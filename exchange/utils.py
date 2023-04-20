from create import available_currencies
from exchange.keyboards import currency_on_page_cnt


def get_max_currency_page():
	"""Возвращает максимальное количество страниц для клавиатуры с валютами."""
	return (currency_on_page_cnt - 1 + len(available_currencies)) // currency_on_page_cnt

def get_picked_currency_msg(currency_code):
	"""Сообщение о том какая валюта для конвертации выбрана."""
	return 'Выбрана валюта: {code}\nВыберите валюту в которую нужно конвертировать\n'.format(code=currency_code)


def get_value_info_msg(base_currency, convert_currency):
	"""Сообщение о том какая пара валют выбрана для конвертации,
	с пердложение ввести занчение для конвертации."""
	return 'Введите сколько валюты {base} вы хотите перевести в {convert}'.format(
		base=base_currency,
		convert=convert_currency,
	)


def is_float(value):
	"""Проверяет является ли число float"""
	try:
		value = float(value)
		return value
	except Exception as e:
		return None