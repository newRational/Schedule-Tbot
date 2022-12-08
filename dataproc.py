import fitz, re
import redis


data_path = 'C:/Python/scripts/tbot/data/'
redis_connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)


def get_redis_db_connection():
	return redis.Redis(connection_pool=redis_connection_pool)


def exists_user_entry(user_id):
	redis = get_redis_db_connection()
	if redis.exists('user:' + str(user_id)):
		return True
	else:
		return False


def set_group_by_user_id(user_id, group_name):
	redis = get_redis_db_connection()
	redis.set('user:' + str(user_id), group_name)


def get_group_by_user_id(user_id):
	redis = get_redis_db_connection()
	group_name = redis.get('user:' + str(user_id)).decode('utf-8')

	return group_name


def verify_group_name(group_name):
	res = re.match('[БСМИ]\d{2}-\d{2,3}', group_name)
	if res: 
		return True
	else:
		return False


def pdf_to_txt(group_name):
	text = get_formated_text(group_name)

	f = open(data_path + group_name + '/schedule.txt', 'w')
	f.write(text)
	f.close()


def load_from_txt(group_name):
	f = open(data_path + group_name + '/schedule.txt')
	text = ''

	for s in f.readlines():
		text += s

	f.close()

	return text


def get_formated_text(group_name):
	pdf_file = get_pdf_file(group_name)
	text = rawtext(pdf_file)
	text = cleantext(text)
	text = separate_classes(text)

	return text 


def get_pdf_file(group_name):
	pdf_file = fitz.open(data_path + group_name + '/schedule.pdf')
	return pdf_file


def rawtext(pdf_file):
	text = ''

	for page in pdf_file:
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