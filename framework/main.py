class AppFramework:

    def __init__(self, urlpatterns: dict, framework_controller: list):
        self.urlpatterns = urlpatterns
        self.framework_controller = framework_controller

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        print(path)

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = {}

            for controller in self.framework_controller:
                controller(request)

                code, text = view(request)
                start_response(code, [('Content-Type', 'text/html')])
                return [text.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'NOT FOUND']
