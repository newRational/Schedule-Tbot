import schedule, telebot

bot = telebot.TeleBot('5833315479:AAFMlEAzJLHzOyY-EsrUvWCKT6vB-ZjxyNg')

def getsch(dayOfWeek):
	try:
		text = schedule.formtext('C:/Python/scripts/files/schedule.pdf')
	except Exception as e:
		return 'Файл с расписанием не найден' + '\n' + str(e)

	return schedule.get_by_day_of_week(text, dayOfWeek)
	
@bot.message_handler(commands=["start"])
def start(m, res=False):
	bot.send_message(m.chat.id, 'Привет, я показываю расписание')

@bot.message_handler(content_types=["text"])
def handle_text(message):
	bot.send_message(message.chat.id, getsch(message.text), parse_mode="Markdown")

bot.polling(none_stop=True, interval=0)
