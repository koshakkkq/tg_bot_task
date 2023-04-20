"""Создание сообщений для меню."""
def get_menu_msg(user_name):
	message = "{name}, Добро пожаловать в бот!".format(
		name=user_name,
	)
	return message

