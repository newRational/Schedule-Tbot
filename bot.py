import schedule, telebot

token = '5833315479:AAFMlEAzJLHzOyY-EsrUvWCKT6vB-ZjxyNg'
bot = telebot.TeleBot(token)

filename = 'S-Б21-505.txt'

def getsch(day_of_week):
	try:
		return schedule.get_schedule(filename, day_of_week)
	except Exception as e:
		return 'Какая-то неполадка :(' + str(e) + ')' 
	
@bot.message_handler(commands=["start"])
def start(m, res=False):
	bot.send_message(m.chat.id, 'Привет, я показываю расписание')

@bot.message_handler(content_types=["text"])
def handle_text(message):
	bot.send_message(message.chat.id, getsch(message.text), parse_mode="Markdown")

bot.polling(none_stop=True, interval=0)
