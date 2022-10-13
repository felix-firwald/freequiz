from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'showbar', 'slug', 'status',
    )


admin.site.register(Notification, NotificationAdmin)
