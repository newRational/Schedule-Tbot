import fitz, re


shorts = {0: ['пн', 'по'], 1: ['вт'], 2: ['ср'], 3: ['чт', 'че'], 4: ['пт', 'пя']}


def getsch(filename):
	text = rawtext(filename)
	text = cleantext(text)
	text = separate_classes(text)
	days = split_by_days(text)

	return days


def rawtext(filename):
	doc = fitz.open(filename)
	text = ''

	for page in doc:
		text += page.get_text()

	return text


def cleantext(text):
	text = re.sub('[■◩◪]', '', text)
	text = re.sub('\(?http[^()]*\)', '', text)
	text = re.sub('\n ', '\n', text)
	text = re.sub('\n,', ',', text)
	text = re.sub('\n\n', '\n', text)
	text = re.sub(get_title(text), '', text)

	return text


def get_title(text):
	title = re.findall('[^_]*ПОНЕДЕЛЬНИК', text)[0]
	title = title.replace('\nПОНЕДЕЛЬНИК', '')

	return title


def separate_classes(text):
	# В auds сохраним все аудитории
	auds = re.findall('\n[А-Я]-\d{3}.?|\nДОТ|\nНЛК-\d{3}|\n\d{3}|\nкаф.*', text)

	# Замени все строки с аудиториями на \n\n
	text = re.sub('\n[А-Я]-\d{3}.?|\nДОТ|\nНЛК-\d{3}|\n\d{3}|\nкаф.*', '\n', text)

	# Выделим академические пары
	classes = text.split('\n\n')

	text = ''

	# Соберем весь текст воедино, добавив в конце записи каждой пары
	# строку с соответствующей аудиторией
	for i in range(0, len(auds)):
		text += classes[i] + auds[i] + '\n\n'

	return text


def split_by_days(text):
	text = re.sub('\nПОНЕДЕЛЬНИК', 'ПОНЕДЕЛЬНИК\n', text)
	text = re.sub('\nВТОРНИК', '\n\n\nВТОРНИК\n', text)
	text = re.sub('\nСРЕДА', '\n\n\nСРЕДА\n', text)
	text = re.sub('\nЧЕТВЕРГ', '\n\n\nЧЕТВЕРГ\n', text)
	text = re.sub('\nПЯТНИЦА', '\n\n\nПЯТНИЦА\n', text)

	days = text.split('\n\n\n')

	return days


def sch_by_dow(days, day_of_week):
	day_ind = get_day_ind(day_of_week)

	if day_ind == -1: 
		return 'Неверный ввод дня недели'

	return days[day_ind]


def get_day_ind(day_of_week):
	day_of_week = day_of_week.lower()

	for x in shorts:
		for y in shorts[x]:
			if re.match(y + '[а-я]*', day_of_week):
				return x

	return -1