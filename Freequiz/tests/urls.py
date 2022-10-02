from django.urls import path
from . import views

app_name = 'tests'

urlpatterns = [
    path('', views.main_page),
    path('create_quiz/', views.create_quiz),
    path('quiz/<slug:slug>/', views.quiz),
    path('quiz/<slug:slug>/delete/', views.delete_quiz),
    path('quiz/<slug:slug>/edit/', views.edit_quiz),
    path('result/<slug:slug>/', views.quiz_result),
]
