import json


def parse_config():
	with open('config.json') as f:
		data = json.load(f)
		return data


def get_available_currencies():
	with open('available_currency.json') as f:
		data = json.load(f)
		return data['currency']

