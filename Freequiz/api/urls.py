from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    QuizList,
    QuizDetail,
    QuestionsViewSet,
    VariantsViewSet,
    ResultsViewSet
)



urlpatterns = [
    path(
        'quiz/', QuizList.as_view()
    ),
    path(
        'quiz/<slug:slug>/', QuizDetail.as_view()
    ),
    path(
        'quiz/<slug:slug>/questions/', QuestionsViewSet.as_view(
            {
                'get': 'list'
            }
        )
    ),
    path(
        'questions/', QuestionsViewSet.as_view(
            {
                'post': 'create',
            }
        )
    ),
    path(
        'questions/<int:pk>/', QuestionsViewSet.as_view(
            {
                'put': 'update',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'variants/', VariantsViewSet.as_view(
            {
                'post': 'create',
            }
        )
    ),
    path(
        'variants/<int:pk>/', VariantsViewSet.as_view(
            {
                'put': 'update',
                'delete': 'destroy'
            }
        )
    ),
    path(
        'quiz/<slug:slug>/results/', ResultsViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })
    )
]
