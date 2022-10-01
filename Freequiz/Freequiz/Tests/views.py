from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def main_page(request):
    return render(
        request,
        'index.html'
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
