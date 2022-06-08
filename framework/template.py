from jinja2 import FileSystemLoader, Environment


def render(template_name, folder='templates', static_url='/static/', **kwargs):
    """
    Работа с шаблонизатором jinja2
    :param template_name: название шаблона
    :param folder: папка с шаблоном
    :param kwargs: параметры, которые передаются в шаблон
    :return:
    """

    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    template = env.get_template(template_name)
    return template.render(**kwargs)
