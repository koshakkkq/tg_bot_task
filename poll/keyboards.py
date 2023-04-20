from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType


poll_button = KeyboardButtonPollType()

poll_buttons = [
	[KeyboardButton(text='Составить опрос', request_poll=poll_button)],
]

poll_keyboard = ReplyKeyboardMarkup(keyboard=poll_buttons)
