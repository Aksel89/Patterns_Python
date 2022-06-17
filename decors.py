"""Декораторы"""
import logging
from datetime import datetime

import logs.fw_log
from patterns.singltone import SingletonByName

# метод определения модуля, источника запуска.
# Метод find () возвращает индекс первого вхождения искомой подстроки,
# если он найден в данной строке.
# Если его не найдено, - возвращает -1.


def log(func_to_log):
    """Функция-декоратор"""
    def log_saver(*args, **kwargs):
        logger_name = 'framework'
        LOGGER = logging.getLogger(logger_name)

        ret = func_to_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}')
        return ret
    return log_saver


def debug(func):
    def msg_in_terminal(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Вызвана функция {func.__name__} из модуля {func.__module__} "
              f"с параметрами {args}, {kwargs}")
        return result
    return msg_in_terminal


class AppRoute:
    def __init__(self, routes, url):

        self.routes = routes
        self.url = url

    def __call__(self, cls):

        self.routes[self.url] = cls


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        print('log: ', text, datetime())
