from framework.template import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


class Contacts:
    def __call__(self, request):
        if request.get('method') == 'POST':
            print(request['data'])
            # data = request['data']
            # name = data['name']
            # text = data['text']
            # email = data['email']

            # if data:
            #     print(f'Получены контактные данные:\n '
            #           f'Имя: {name} \n '
            #           f'Сообщение: {text} \n '
            #           f'email: {email}')
            return '200 OK', render('contacts.html')
        else:
            return '200 OK', render('contacts.html')
