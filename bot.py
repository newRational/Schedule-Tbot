import dataproc, schedule, telebot, config


token = '5833315479:AAFMlEAzJLHzOyY-EsrUvWCKT6vB-ZjxyNg'
bot = telebot.TeleBot(token)

	
@bot.message_handler(commands=['start'])
def start(m, res=False):
	bot.send_message(m.chat.id, 'Привет, я показываю расписание.')


@bot.message_handler(commands=['set_group'])
def set_group(m, res=False):
	msg = bot.send_message(m.chat.id, 'Введите учебную группу')
	bot.register_next_step_handler(msg, config.set_group_name)


@bot.message_handler(content_types=['text'])
def handle_weekday(message):
	handle_user(message)
	response = ''
	
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
