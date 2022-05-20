from wsgiref.simple_server import make_server

from framework.main import AppFramework
from urls import routes, fronts

application = AppFramework(routes, fronts)
app_ip = '127.0.0.1'
app_port = int(input('На каком порту запустить сервер?>>> '))


def server_run():
    with make_server(app_ip, app_port, application) as httpd:
        print(f'Сервер запущен по адресу: {app_ip}:{app_port}')
        httpd.serve_forever()


if __name__ == '__main__':
    server_run()
