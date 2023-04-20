import logging

from aiogram import executor
from create import dp, bot
from register_handlers import handler_register

logging.basicConfig(
	level=logging.ERROR,
	format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s',
	datefmt='%Y-%m-%d:%H:%M:%S',
	filename='log.txt'
)

handler_register(dp)


executor.start_polling(dp, skip_updates=True)
