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
    tests = BlueprintTest.objects.filter(
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
    # BlueprintTest.objects.filter().get()
    if test.is_closed is True:
        context = {
            'result': False
        }
    else:
        context = {
            'result': True,
            'slug': slug,
            'id': test.questions.all()[0]
        }
    return render(
        request,
        'start_test.html',
        context
    )


@login_required
def question(request, slug, question_id):
    question = BlueprintQuestion.objects.filter(
        pk=question_id,
        test__slug=slug,
        test__is_closed=False
    )
    if not question:
        return redirect(
            'tests:main'
        )
    return render(
        request,
        'question.html',
        {'question': question[0]}
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
        {'data': result}
    )
