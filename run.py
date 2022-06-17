from wsgiref.simple_server import make_server

from framework.main import AppFramework, DebugApplication
from views import routes

application = AppFramework(routes)
# application = DebugApplication(routes)
app_ip = '127.0.0.1'
app_port = int(input('На каком порту запустить сервер?>>> '))


with make_server(app_ip, app_port, application) as httpd:
    print(f'Сервер запущен по адресу: {app_ip}:{app_port}')
    httpd.serve_forever()



