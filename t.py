import schedule

d = {'ПН': 1, 'ВТ': 2, 'СР': 3, 'ЧТ': 4, 'ПТ': 5}

if 0:
	for x in schedule.formtext('C:/Python/scripts/files/schedule.pdf'):
		print(x)
else:
	days = schedule.formtext('C:/Python/scripts/files/schedule.pdf')
	print(schedule.get_by_day_of_week(days, 'ПН'))