from aiogram import types, Dispatcher
import menu
import weather
import exchange
import pictures
import poll

def handler_register(dp: Dispatcher):
	menu.handler_register(dp)
	weather.handler_register(dp)
	exchange.handler_register(dp)
	pictures.handler_register(dp)
	poll.handler_register(dp)