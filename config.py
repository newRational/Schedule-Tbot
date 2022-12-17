import dataproc


def token_from_db():
	rdb = dataproc.get_redis_db_connection()
	return rdb.get('telebot:token').decode('utf-8')


def set_group_name(message):
	user_id = message.from_user.id
	group_name = message.text
	dataproc.set_group_by_user_id(user_id, group_name)