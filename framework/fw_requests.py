class GetRequest:

    @staticmethod
    def parser_input_data(data: str):
        query_param = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                if query_param.get(k):
                    query_param[k].append(v)
                else:
                    query_param[k] = [v]
        return query_param

    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        print(query_string)
        request_params = GetRequest.parser_input_data(query_string)
        return request_params


class PostRequest:

    @staticmethod
    def parse_input_data(data: str):
        query_param = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                if query_param.get(k):
                    query_param[k].append(v)
                else:
                    query_param[k] = [v]
        return query_param

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:

        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:

        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):

        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data
