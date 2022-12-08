import dataproc


def set_group_name(message):
	user_id = message.from_user.id
	group_name = message.text
	dataproc.set_group_by_user_id(user_id, group_name)

	print('Группа', group_name, 'успешно установлена')