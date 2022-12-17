import dataproc, schedule, telebot, config, buttons
from telebot import types


token = config.token_from_db()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message, res=False):
	markup = buttons.group_buttons_markup()
	bot.send_message(message.chat.id, 
		'Привет, я показываю расписание\nВыбирай группу',
		reply_markup=markup)


@bot.message_handler(regexp='Выбрать группу')
def pick_group(message):
	markup = buttons.group_buttons_markup()
	bot.send_message(message.chat.id, 'Выбирай группу', reply_markup=markup)


@bot.message_handler(regexp='[БСМИ]\d{2}-\d{2,3}')
def pick_day(message):
	config.set_group_name(message)
	markup = buttons.weekday_buttons_markup()
	bot.send_message(message.chat.id, 'Выбирай день недели', reply_markup=markup)


@bot.message_handler(regexp='[Пп]н.*|[Пп]он.*|[Вв]т.*|[Сс]р.*|[Чч]т.*|[Чч]ет.*|[Пп]т.*|[Пп]ят.*|[Сс]б.*|[Сс]уб.*|[Сс]е.*')
def handle_weekday(message):
	response = schedule.get_schedule(message.from_user.id, message.text)
	bot.send_message(message.chat.id, text=response, parse_mode="Markdown")


bot.polling(none_stop=True, interval=0)