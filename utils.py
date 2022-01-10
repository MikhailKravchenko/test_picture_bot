# -*- coding: utf-8 -*-
import shelve
from config import shelve_name

# Запись данных в хранилище
def set_user_dict(chat_id, args):
    """

    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = args


# Чтение данных из хранилища
def get_user_dict(chat_id):
    """

    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        except KeyError:
            return None




