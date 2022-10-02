from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import (
    User,
    Variant,
    Question,
    Test,
    Result
)


def main_page(request):
    tests = Test.objects.filter(
        is_closed=False,
        access='all'
    )
    return render(
        request,
        'index.html',
        {'tests': tests}
    )


@login_required
def create_quiz(request):
    pass


@login_required
def quiz(request):
    pass


@login_required
def delete_quiz(request):
    pass


@login_required
def edit_quiz(request):
    pass


def quiz_result(request):
    pass
