import os
from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    Работа с шаблонизатором jinja2
    :param template_name: название шаблона
    :param folder: папка с шаблоном
    :param kwargs: параметры, которые передаются в шаблон
    :return:
    """

    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)
