import quopri
from framework.input_data import DecoderInputData
from framework.fw_requests import GetRequest, PostRequest, PageNotFound404
from logs.fw_log import LOGGER


class AppFramework:

    def __init__(self, routes_obj):
        self.routes_lst = routes_obj

    def __call__(self, env, start_response):
        path = env['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = env['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request_params(env)
            request['data'] = data
            print(f'Пришел POST-запрос: {DecoderInputData.decode_value(data)}')
            LOGGER.debug(f'Нам пришёл post-запрос: '
                         f'{DecoderInputData.decode_value(data)}')

        if method == 'GET':
            request_params = GetRequest().get_request_params(env)
            request['request_params'] = request_params
            print(f'Пришли GET-параметры:{request_params}')
            LOGGER.debug(f'Нам пришли GET-параметры: {request_params}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
            print(view)
        else:
            view = PageNotFound404()

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


class DebugApplication(AppFramework):

    def __init__(self, routes_obj):
        self.application = AppFramework(routes_obj)
        super().__init__(routes_obj)

    def __call__(self, environ, start_response):
        print('DEBUG MODE')
        print(environ)
        return self.application(environ, start_response)
