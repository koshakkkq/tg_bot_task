import logging
import time

from aiogram import types
from create import db_tg_task
import hashlib

polls_coll = db_tg_task.polls


async def get_poll_id_msg(poll, msg_id, chat_id):
	try:
		time_stamp = str(time.time())
		poll_id_to_hash = '{poll}{msg_id}{stamp}'.format(
			poll=poll,
			msg_id=msg_id,
			stamp=time_stamp,
		)

		hash_id = hashlib.sha1(poll_id_to_hash.encode())

		hash_id = hash_id.hexdigest()

		hash_id = hash_id[:10]

		poll_dict = create_dict_from_poll(poll)

		await polls_coll.insert_one({'id': hash_id, 'poll': poll_dict})

		response_msg = 'Добавьте бота в групповой чат и введите команду /poll_{hash_id}'.format(
			hash_id=hash_id,
		)
		response_msg += '\n\nКоманда будет работать один вызов!'
		response_msg += '\nУ бота должен быть доступ к сообщениям.'
		return response_msg
	except Exception as e:
		logging.error(e)
		return 'Ошибка на сервере!'


def create_dict_from_poll(poll: types.Poll):
	options = []
	for i in poll.options:
		options.append(i['text'])
	res_dict = {
		'question': poll.question,
		'options': options,
		'type': poll.type,
		'is_anonymous': poll.is_anonymous,
		'allows_multiple_answers': poll.allows_multiple_answers,
		'correct_option_id': poll.correct_option_id,
		'explanation': poll.explanation,
		'open_period': poll.open_period,
		'close_date': poll.close_date,
		'is_closed': poll.is_closed,
	}
	return res_dict


async def get_poll_from_command(command: str):
	poll_id = command.split('_')[-1]
	try:
		poll_doc = await polls_coll.find_one({'id': poll_id})
		response_poll = poll_doc['poll']
		return response_poll

	except Exception as e:
		logging.error(e)
		return None


async def delete_poll(command: str):
	poll_id = command.split('_')[-1]
	try:
		await polls_coll.delete_one({'id': poll_id})
	except Exception as e:
		logging.error(e)
