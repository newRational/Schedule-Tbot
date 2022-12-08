import re, dataproc


jam = 'q5^$@*QUR*W'


def bold(string):
	return '*' + string + '*'


def bold_day_name(day):
	day_name = re.findall('[А-Я]{5,11}', day)[0]
	day = re.sub('[А-Я]{5,11}', bold(day_name), day)

	return day


def bold_time_periods(day):
	# В time_periods сохраним все периоды времени
	time_periods = re.findall('\d{2}:\d{2} — \d{2}:\d{2}', day)

	# Замени все строки с периодами времени на jam-последовательность
	day = re.sub('\d{2}:\d{2} — \d{2}:\d{2}', jam, day)

	# Выделим академические пары
	classes = day.split(jam)

	day = classes[0]

	# Соберем весь текст воедино, добавив в начале записи каждой пары
	# строку с соответствующим временным периодом. 
	# Начинаем с 1, т.к под 0 индексом стоит название дня недели
	for i in range(0, len(time_periods)):
		day += bold(time_periods[i]) + classes[i+1]

	return day.strip()


def bold_classrooms(day):
	# В classrooms сохраним все аудитории
	classrooms = re.findall('\n[А-Я]-\d{3}.?|\nДОТ|\nНЛК-\d{3}|\n\d{3}|\nкаф.*', day)

	# Замени все строки с аудиториями на \n\n
	day = re.sub('\n[А-Я]-\d{3}.?|\nДОТ|\nНЛК-\d{3}|\n\d{3}|\nкаф.*', jam, day)

	# Выделим академические пары
	classes = day.split(jam)

	day = ''

	# Соберем весь текст воедино, добавив в конце записи каждой пары
	# строку с соответствующей аудиторией
	for i in range(0, len(classrooms)):
		day += classes[i] + bold(classrooms[i])

	return day.strip()