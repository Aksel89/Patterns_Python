from framework.input_data import DecoderInputData
from framework.fw_requests import GetRequest, PostRequest, PageNotFound404
from logging import getLogger


LOGGER = getLogger('AppFramework')


class AppFramework:

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
            print(f'Пришел POST-запрос: {DecoderInputData.decode_value(data)}')
            LOGGER.info(f'Нам пришёл post-запрос: {DecoderInputData.decode_value(data)}')

        if method == 'GET':
            request_params = GetRequest().get_request_params(env)
            request['request_params'] = request_params
            print(f'Пришли GET-параметры:{request_params}')
            LOGGER.info(f'Нам пришли GET-параметры: {request_params}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
            print(view)
        else:
            view = PageNotFound404()

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
