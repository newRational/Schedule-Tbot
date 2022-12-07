import schedule

d = {'ПН': 1, 'ВТ': 2, 'СР': 3, 'ЧТ': 4, 'ПТ': 5}

filename = 'schedule.pdf'

def raw_test(filename):
	text = schedule.rawtext(filename)
	print(text)

def clean_test(filename):
	text = schedule.rawtext(filename)
	text = schedule.cleantext(text)
	text = schedule.separate_classes(text)
	print(text)

def by_day_test(filename):
	days = schedule.getsch(filename)
	text = schedule.sch_by_dow(days, 'пон')
	print(text)

# raw_test(filename)
# clean_test(filename)
by_day_test(filename)

