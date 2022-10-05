from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import (
    User,
    Variant,
    BlueprintQuestion,
    Question,
    BlueprintTest,
    Test,
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
def question(request, slug, pk):
    question = Question.objects.get(pk=pk)
    context = {
        'question': question,
        'slug': slug
    }

    return render(
        request,
        'question.html',
        context
    )


@login_required
def quiz(request, slug):
    test = get_object_or_404(
        BlueprintTest,
        slug=slug
    )
    if test.is_closed is True:
        context = {
            'result': False
        }
    else:
        context = {
            'result': True,
            'content': test.questions.all(),
        }
    return render(
        request,
        'question.html',
        context
    )


@login_required
def delete_quiz(request, slug):
    test = get_object_or_404(
        BlueprintTest,
        slug=slug
    )
    if test.author == request.user:
        test.delete()
        return redirect(
            'tests:main'
        )
    return redirect(
        'tests:quiz',
        slug
    )


@login_required
def edit_quiz(request):
    pass


def quiz_result(request, slug):
    result = get_object_or_404(
        Test,
        slug=slug
    )
    return render(
        request,
        'result.html',
        result
    )
