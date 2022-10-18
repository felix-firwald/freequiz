from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import QuizList, QuizDetail, QuestionsViewSet, ResultsViewSet

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
        'questions/<int:pk>/', QuestionsViewSet.as_view({
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'perform_destroy'
        })
    ),
    path(
        'quiz/<slug:slug>/questions/', QuestionsViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path('quiz/<slug:slug>/results/', ResultsViewSet.as_view({
        'get': 'list',
        'post': 'create'
        })
    )
]
