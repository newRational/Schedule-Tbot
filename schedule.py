import fitz, re, fmtpdf, style


shorts = {0: ['пн', 'по'], 1: ['вт'], 2: ['ср'], 3: ['чт', 'че'], 4: ['пт', 'пя']}
data_path = 'C:/Python/scripts/tbot/data/'


def get_schedule(filename_txt, day_of_week):
	text = fmtpdf.load_from_txt(filename_txt)
	days = split_by_days(text)
	day = sch_by_dow(days, day_of_week)
	day = modify_day(day)

	return day


def modify_day(day):
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

	days = text.split('\n\n\n')

	return days


def sch_by_dow(days, day_of_week):
	day_ind = get_day_ind(day_of_week)

	if day_ind == -1: 
		return 'Неверный ввод дня недели'

	return days[day_ind].strip()


def get_day_ind(day_of_week):
	day_of_week = day_of_week.lower()

	for x in shorts:
		for y in shorts[x]:
			if re.match(y + '[а-я]*', day_of_week):
				return x

	return -1