from views import Index, About


routes = {
    '/': Index(),
    '/about/': About(),
}


def key_front(request):
    request['key'] = 'key'


fronts = [key_front]
