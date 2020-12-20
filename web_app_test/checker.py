from flask import session
from functools import wraps


def check_logged_in(func):
    """
    Функиция-декоратор для проверки входа пользователя в систему
    используя словарь значений session.

    :param func: принимаемая функция
    :return: декорируемая функция или функция-обертка.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return 'You are NOT logged in.'

    return wrapper
