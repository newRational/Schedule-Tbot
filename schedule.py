import fitz, re, dataproc, style, time


shorts = {0: ['пн', 'по'], 1: ['вт'], 2: ['ср'], 3: ['чт', 'че'], 4: ['пт', 'пя'], 5: ['сб', 'су'], 6: ['вс', 'во']}
data_path = 'C:/Python/scripts/tbot/data/'


def text_by_user_id(user_id):
	group_name = dataproc.get_group_by_user_id(user_id)
	text = dataproc.sch_from_rdb(group_name)

	return text


def get_schedule(user_id, weekday):
	try:
		text = text_by_user_id(user_id)
		days = split_by_days(text)
		day = sch_by_day(days, weekday)
		day = style_sch(day)
	except Exception as e:
		day = str(e)

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

	try:
		return days[day_ind].strip()
	except Exception as e:
		raise Exception('У тебя нет пар в выбранный день')

	return days[day_ind].strip()


def get_day_ind(weekday):
	weekday = weekday.lower()

	for day_ind in shorts:
		for short in shorts[day_ind]:
			if re.match(short + '[а-я]*', weekday):
				return day_ind

	if re.match('се[а-я]*', weekday):
		return get_today_day_ind(weekday)

	return -1


def get_today_day_ind(weekday):
	now = time.localtime()
	return now.tm_wday