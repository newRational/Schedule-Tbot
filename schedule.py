import fitz, re

shorts = {1: ['пн', 'по'], 2: ['вт'], 3: ['ср'], 4: ['чт', 'че'], 5: ['пт', 'пя']}
dn = {1: 'ПОНЕДЕЛЬНИК', 2: 'ВТОРНИК', 3: 'СРЕДА', 4: 'ЧЕТВЕРГ', 5: 'ПЯТНИЦА'}


auds = list()


def formtext(filename):
	doc = fitz.open(filename)
	text = ''

	for page in doc:
		text += page.get_text()

	text = re.sub('[■◩◪]', '', text)
	text = re.sub('\(h.*\)', '', text)
	text = re.sub('\(.*,\nh.*\)', '', text)
	text = re.sub('\n ', '\n', text)
	text = re.sub('\n,', ',', text)
	text = re.sub('\n\n', '\n', text)

	text = re.sub('\nПОНЕДЕЛЬНИК', '\n\n\n*ПОНЕДЕЛЬНИК', text)
	text = re.sub('\nВТОРНИК', '\n\n\n*ВТОРНИК', text)
	text = re.sub('\nСРЕДА', '\n\n\n*СРЕДА', text)
	text = re.sub('\nЧЕТВЕРГ', '\n\n\n*ЧЕТВЕРГ', text)
	text = re.sub('\nПЯТНИЦА', '\n\n\n*ПЯТНИЦА', text)

	text = re.sub('\nПР', '\n*ПР*', text)
	text = re.sub('\nЛЕК', '\n*ЛЕК*', text)
	text = re.sub('\nЛАБ', '\n*ЛАБ*', text)

	days = text.split('\n\n\n')

	return days


def get_by_day_of_week(days, dayOfWeek):
	day_ind = get_day_ind(dayOfWeek)

	if day_ind == -1: 
		return 'Неверный ввод дня недели'

	day = days[day_ind]
	
	auds = re.findall('\n[А-Я]-\d{3}.?|\nДОТ|\nНЛК-\d{3}|\n\d{3}|\nкаф. 15/3', day)

	l = len(auds)

	day = re.sub('\n[А-Я]-\d{3}.?|\nДОТ|\nНЛК-\d{3}|\n\d{3}|\nкаф. 15/3', '\n\n', day)

	pairs = day.split('\n\n')

	full = ''

	for i in range(0, l):
		pairs[i] += auds[i] + '\n'

	for i in range(0, l):
		full += pairs[i]

	full = re.sub('[A-Я]{5,11}', dn[day_ind] + '*\n', full).strip()

	print(full)

	return full


def get_day_ind(dayOfWeek):
	dayOfWeek = dayOfWeek.lower()

	for x in shorts:
		for y in shorts[x]:
			if re.match(y + '[а-я]*', dayOfWeek):
				return x

	return -1