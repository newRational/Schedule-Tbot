import fitz, re


data_path = 'C:/Python/scripts/tbot/data/'


def pdf_to_txt(filename_pdf):
	text = get_correct_text(filename_pdf)
	filename_txt = filename_pdf.replace('.pdf', '.txt')

	f = open(data_path + filename_txt, 'w')
	f.write(text)
	f.close()


def load_from_txt(filename_txt):
	f = open(data_path + filename_txt)
	text = ''

	for s in f.readlines():
		text += s

	f.close()

	return text


def get_correct_text(filename_pdf):
	text = rawtext(filename_pdf)
	text = cleantext(text)
	text = separate_classes(text)

	return text 


def rawtext(filename_pdf):
	doc = fitz.open(data_path + filename_pdf)
	text = ''

	for page in doc:
		text += page.get_text()

	return text


def cleantext(text):
	text = re.sub('[■◩◪]', '', text)
	text = re.sub('\(?http[^()]*\)', '', text)
	text = re.sub(' ', ' ', text)
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
	# В classrooms сохраним все аудитории
	classrooms = re.findall('\n[А-Я]-\d{3}.?|\nДОТ|\nНЛК-\d{3}|\n\d{3}|\nкаф.*', text)

	# Замени все строки с аудиториями на \n\n
	text = re.sub('\n[А-Я]-\d{3}.?|\nДОТ|\nНЛК-\d{3}|\n\d{3}|\nкаф.*', '\n', text)

	# Выделим академические пары
	classes = text.split('\n\n')

	text = ''

	# Соберем весь текст воедино, добавив в конце записи каждой пары
	# строку с соответствующей аудиторией
	for i in range(0, len(classrooms)):
		text += classes[i] + classrooms[i] + '\n\n'

	return text.strip()