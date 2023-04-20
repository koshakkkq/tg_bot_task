"""Фильтр, для определения типа чата."""


def is_chat_private(msg):
	return msg.chat.id > 0


def is_chat_non_private(msg):
	return msg.chat.id < 0
