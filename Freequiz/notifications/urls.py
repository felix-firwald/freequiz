from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path(
        'notification/<slug:slug>',
        views.notification_watch,
        name='watch'
    ),
    path(
        'notification_was_seen/<int:pk>',
        views.notification_was_seen,
        name='seen'
    )
]
