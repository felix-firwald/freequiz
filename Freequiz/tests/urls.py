from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path(
        '',
        views.main_page,
        name='main'
    ),
    path(
        'create_quiz/',
        views.create_quiz,
        name='create_quiz'
    ),
    path(
        'quiz/<slug:slug>/',
        views.quiz,
        name='quiz'
    ),
    path(
        'quiz/<slug:slug>/data',
        views.get_data_for_quiz,
        name='get_data_for_quiz'
    ),
    path(
        'quiz/<slug:slug>/delete/',
        views.delete_quiz,
        name='delete_quiz'
    ),
    path(
        'quiz/<slug:slug>/edit/',
        views.edit_quiz,
        name='edit_quiz'
    ),
    path(
        'result/<slug:slug>/',
        views.quiz_result,
        name='result'
    ),
    path(
        'my_results',
        views.my_results,
        name='my_results'
    )
]
