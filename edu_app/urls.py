from django.urls import path
from .views import instructor_dashboard, available_courses, enroll_course, update_progress, student_page, index, user_login, register, course_list, create_course, update_course, delete_course

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('courses/', course_list, name='course_list'),
    path('courses/create/', create_course, name='create_course'),
    path('courses/<int:course_id>/update/', update_course, name='update_course'),
    path('courses/<int:course_id>/delete/', delete_course, name='delete_course'),
    path('dashboard/', instructor_dashboard, name='instructor_dashboard'),
    path('student/', student_page, name='student_page'),
    path('courses/<int:course_id>/enroll/', enroll_course, name='enroll_course'),
    path('enrollment/<int:enrollment_id>/update/', update_progress, name='update_progress'),
    path('available_courses/', available_courses, name='available_courses'),
]
