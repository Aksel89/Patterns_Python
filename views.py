from datetime import date
from logging import getLogger

from patterns.cbv import ListView, CreateView
from decors import AppRoute, Logger, debug
from framework.main import AppFramework, DebugApplication
from framework.template import render
from patterns.creational_patterns import Engine
from framework.fw_requests import GetRequest


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
class CreateCategory(CreateView):
    template_name = 'create-category.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_category(name)
        site.categories.append(new_obj)
        LOGGER.info(f'Добавлена категория {name}')


@AppRoute(routes=routes, url='/category-list/')
class CategoryList(ListView):
    queryset = site.categories
    template_name = 'category-list.html'


@AppRoute(routes=routes, url='/student-list/')
class StudentList(ListView):
    queryset = site.students
    template_name = 'student-list.html'


@AppRoute(routes=routes, url='/create-student/')
class StudentCreate(CreateView):
    template_name = 'create-student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        LOGGER.info(f'Добавлен студент {name}')


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourse(CreateView):
    template_name = 'add-student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)
        LOGGER.info(f'Студент {student_name} записан на курс {course_name}')
