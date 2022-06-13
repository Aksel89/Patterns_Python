"""Декоратор"""

import sys
import logging
import logs.fw_log

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
