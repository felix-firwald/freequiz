from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Notification, Delivered


@login_required
def notification_was_seen(request, pk):
    try:
        notif = Notification.objects.get(pk=pk)
        Delivered.objects.create(
            user=request.user,
            notification=notif
        )

    except Exception as ex:
        return JsonResponse(
            {'success': False, 'error': ex}
        )
    else:
        return JsonResponse(
            {'success': True}
        )


def notification_watch(request, slug):
    notif = get_object_or_404(Notification, slug=slug)
    return render(
        request,
        'notification.html',
        {
            'name': notif.name,
            'details': notif.details,
            'color': notif.status
        }
    )
