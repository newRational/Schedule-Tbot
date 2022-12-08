import fitz, re, dataproc, style, time


shorts = {0: ['пн', 'по'], 1: ['вт'], 2: ['ср'], 3: ['чт', 'че'], 4: ['пт', 'пя'], 5: ['су'], 6: ['вс', 'во']}
data_path = 'C:/Python/scripts/tbot/data/'


def sch_by_id(user_id):
	group_name = dataproc.get_group_by_user_id(user_id)
	text = dataproc.load_from_txt(group_name)

	return text


def get_schedule(user_id, weekday):
	text = sch_by_id(user_id)
	days = split_by_days(text)
	day = sch_by_day(days, weekday)
	day = style_sch(day)

	return day


def style_sch(day):
	day = style.bold_day_name(day)
	day = style.bold_time_periods(day)
	day = style.bold_classrooms(day)

	return day


def split_by_days(text):
	text = re.sub('ПОНЕДЕЛЬНИК', 'ПОНЕДЕЛЬНИК\n', text)
	text = re.sub('\nВТОРНИК', '\n\n\nВТОРНИК\n', text)
	text = re.sub('\nСРЕДА', '\n\n\nСРЕДА\n', text)
	text = re.sub('\nЧЕТВЕРГ', '\n\n\nЧЕТВЕРГ\n', text)
	text = re.sub('\nПЯТНИЦА', '\n\n\nПЯТНИЦА\n', text)
	text = re.sub('\nСУББОТА', '\n\n\nСУББОТА\n', text)

	days = text.split('\n\n\n')

	return days


def sch_by_day(days, weekday):
	day_ind = get_day_ind(weekday)

	if day_ind == -1: 
		raise Exception('Неверный ввод дня недели')

	if day_ind == 6:
		raise Exception('Воу, в воскресенье отдыхать надо, дружище')

	return days[day_ind].strip()


def get_day_ind(weekday):
	weekday = weekday.lower()

	for x in shorts:
		for y in shorts[x]:
			if re.match(y + '[а-я]*', weekday):
				return x

	if re.match('се[а-я]*', weekday):
		return get_today_day_ind(weekday)

	return -1


def get_today_day_ind(weekday):
	now = time.localtime()
	return now.tm_wday