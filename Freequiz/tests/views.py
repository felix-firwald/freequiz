from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import (
    User,
    Variant,
    BlueprintQuestion,
    Question,
    BlueprintTest,
    Test,
)
from notifications.models import Notification


def main_page(request):
    alert = Notification.objects.last()
    tests = BlueprintTest.objects.filter(
        is_closed=False,
        access='all'
    )
    return render(
        request,
        'index.html',
        {
            'tests': tests,
            'notification': alert
        }
    )


@login_required
def create_quiz(request):
    return redirect(
        'tests:main'
    )


@login_required
def get_data_for_quiz(request, slug):
    quiz = get_object_or_404(
        BlueprintTest,
        slug=slug
    )
    questions_list = list()
    for question in quiz.get_guestions():
        variants = []
        for variant in question.get_variants(text_only=True):
            variants.append(variant)
        questions_list.append({question.text: variants})

    return JsonResponse(
        {
            'questions': questions_list,
            'timelimit': int(quiz.timelimit)
        }
    )


@login_required
def quiz(request, slug):
    quiz = get_object_or_404(
        BlueprintTest,
        slug=slug
    )
    context = {
        'slug': quiz.slug,
        'is_closed': quiz.is_closed,
        'name': quiz.name,
        'description': quiz.description,
        'timelimit': quiz.timelimit
    }
    return render(
        request,
        'start_test.html',
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
    return redirect(
        'tests:main'
    )


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


@login_required
def my_results(request):
    results = request.user.tests_results.all()
    return render(
        request,
        'my_results',
        {'data': results}
    )
