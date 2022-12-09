import dataproc, schedule, telebot, config, buttons
from telebot import types


token = config.get_token_from_db()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(m, res=False):

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	
	item1 = types.KeyboardButton('Б21-505')
	item2 = types.KeyboardButton('Б21-514')

	markup.add(item1, item2)

	bot.send_message(m.chat.id, 'Привет, я показываю расписание. \nВыбирай свою группу', reply_markup=markup)


@bot.message_handler(regexp='[БСМИ]\d{2}-\d{2,3}')
def pick_day(message):

	config.set_group_name(message)
	
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	day1 = types.KeyboardButton('Понедельник')
	day2 = types.KeyboardButton('Вторник')
	day3 = types.KeyboardButton('Среда')
	day4 = types.KeyboardButton('Четверг')
	day5 = types.KeyboardButton('Пятница')
	day6 = types.KeyboardButton('Суббота')

	markup.add(day1, day2, day3, day4, day5, day6)

	bot.send_message(message.chat.id, 'Выбирай день недели', reply_markup=markup)


@bot.message_handler(regexp='[Пп]н.*|[Пп]он.*|[Вв]т.*|[Сс]р.*|[Чч]т.*|[Чч]ет.*|[Пп]т.*|[Пп]ят.*|[Сс]б.*|[Сс]уб.*|[Сс]е.*')
def handle_weekday(message):
	handle_user(message)
	
	try:
		response = schedule.get_schedule(message.from_user.id, message.text)
	except Exception as e:
		response = str(e)

	bot.send_message(message.chat.id, text=response, parse_mode="Markdown")


def handle_user(message):
	exists_user = dataproc.exists_user_entry(message.from_user.id)

	if not exists_user:
		set_group(message)


bot.polling(none_stop=True, interval=0)