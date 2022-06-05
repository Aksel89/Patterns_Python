import quopri

from framework.fw_requests import GetRequest, PostRequest


class PageNotFound404:
    def __call__(self, request):
        return '404', '404 PAGE NOT FOUND'


class AppFramework:

    # def __init__(self, urlpatterns: dict, framework_controller: list):
    #     self.urlpatterns = urlpatterns
    #     self.framework_controller = framework_controller
    #     print(urlpatterns)
    #     print(framework_controller)
    def __init__(self, routes_obj):
        self.routes_lst = routes_obj

    def __call__(self, env, start_response):
        path = env['PATH_INFO']
        print(path)

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = env['REQUEST_METHOD']
        print(method)
        request['method'] = method
        print(request)

        if method == 'POST':
            data = PostRequest().get_request_params(env)
            request['data'] = data
            print(f'Пришел POST-запрос: {AppFramework.decode_value(data)}')

        if method == 'GET':
            request_params = GetRequest().get_request_params(env)
            request['request_params'] = request_params
            print(f'Пришли GET-параметры:{request_params}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
            print(view)
        else:
            view = PageNotFound404()

        # for front in self.framework_controller:
        #     front(request)
        # if path in self.routes_object:
        #     print(self.routes_object)
        #     view = self.routes_object[path]
        #     print(view)
        # else:
        #     view = PageNotFound404()

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        decoding_data = {}
        for k, v in data.items():
            print(v)
            value = bytes(v.replace('%', '=').replace('+', ' '), 'utf-8')
            print(value)
            decode_string = quopri.decodestring(value).decode('utf-8')
            decoding_data[k] = decode_string
        return decoding_data
