from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuizList, QuizDetail, QuestionsViewSet

app_name = 'api'

# router = DefaultRouter()
# router.register(r'questions', QuestionsViewSet, basename='questions')

urlpatterns = [
    path(
        'quiz/', QuizList.as_view()
    ),
    path(
        'quiz/<slug:slug>/', QuizDetail.as_view()
    ),
    path(
        'questions/<int:pk>/', QuestionsViewSet.as_view({'delete': 'perform_destroy'})
    ),
    path(
        'quiz/<slug:slug>/questions/', QuestionsViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
]
