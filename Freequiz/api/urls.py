from django.urls import path

from .views import QuizList, QuizDetail

app_name = 'api'

urlpatterns = [
    path(
        'quiz/', QuizList.as_view()
    ),
    path(
        'quiz/<slug:slug>/', QuizDetail.as_view()
    )
]
