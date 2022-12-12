import dataproc
from telebot import types


def group_buttons_markup():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	group_buttons = create_group_buttons()

	markup.add(*group_buttons)

	return markup


def create_group_buttons():
	rdb = dataproc.get_redis_db_connection()
	groups = rdb.smembers('groups')
	group_buttons = []

	for group in groups:
		button = types.KeyboardButton(group.decode('utf-8'))
		group_buttons.append(button)

	return group_buttons


def weekday_buttons_markup():
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	weekday_buttons = create_weekday_buttons()
	
	markup.add(types.KeyboardButton('Сегодня'))
	markup.add(*weekday_buttons)
	markup.add(types.KeyboardButton('Выбрать группу'))

	return markup


def create_weekday_buttons():
	rdb = dataproc.get_redis_db_connection()
	weekdays = rdb.lrange('weekdays', 0, -1)
	weekday_buttons = []

	for weekday in weekdays:
		button = types.KeyboardButton(weekday.decode('utf-8'))
		weekday_buttons.append(button)

	return weekday_buttons


