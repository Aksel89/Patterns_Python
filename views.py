from datetime import date
from logging import getLogger

from decors import AppRoute, Logger, debug
from framework.main import DebugApplication
from framework.template import render
from patterns.creational_patterns import Engine


site = Engine()
LOGGER = getLogger('framework')
routes = {}


@AppRoute(routes=routes, url='/index/')
class Index:
    @debug
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(routes=routes, url='/contacts/')
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


@AppRoute(routes=routes, url='/training-programs/')
class TrainingPrograms:
    @debug
    def __call__(self, request):
        return '200 OK', render('training-programs.html', data=date.today())


class NotFound404:
    @debug
    def __call__(self, request):
        LOGGER.error(f'Ошибка 404. Страница не найдена')
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/course-list/')
class CoursesList:
    @debug
    def __call__(self, request):

        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            LOGGER.info(f'Добавлена категория {category}')
            return '200 OK', render('course-list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            LOGGER.info(f'Нет курса для добавления')
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @debug
    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course-list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                print(f'ахх {request}')
                LOGGER.info(f'Запрос {request}')
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                LOGGER.info(f'Нет категории для добавления')
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @debug
    def __call__(self, request):

        if request['method'] == 'POST':

            print(request)
            LOGGER.info(f'Запрос {request}')
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html',
                                    objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create-category.html',
                                    categories=categories)


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @debug
    def __call__(self, request):
        return '200 OK', render('category-list.html',
                                objects_list=site.categories)