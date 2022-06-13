from views import Index, About, Contacts, TrainingPrograms, CoursesList, \
    CreateCourse, CreateCategory, CategoryList


routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/training-programs/': TrainingPrograms(),
    '/course-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList()
}
