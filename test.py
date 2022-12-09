import schedule, dataproc


d = {'ПН': 1, 'ВТ': 2, 'СР': 3, 'ЧТ': 4, 'ПТ': 5}


group_name = 'Б21-514'
pdf_file = dataproc.get_pdf_file(group_name)


def raw_test(filename):
	text = schedule.rawtext(filename)
	print(text)


def clean_test(pdf_file):
	text = dataproc.rawtext(pdf_file)
	text = dataproc.cleantext(text)
	text = dataproc.separate_classes(text)
	print(text)


def by_day_test(filename):
	print(schedule.get_schedule('S-Б21-505.txt', 'пон'))


# raw_test(filename)
clean_test(pdf_file)
# by_day_test(filename)

