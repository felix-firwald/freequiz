from random import shuffle
import json

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import (
    User,
    Variant,
    BlueprintQuestion,
    Question,
    BlueprintTest,
    Result,
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
        for variant in question.get_variants():
            variants.append([variant.id, variant.text])
        shuffle(variants)
        questions_list.append({question.text: variants})
    shuffle(questions_list)

    return JsonResponse(
        {
            'questions': questions_list,
            'timelimit': int(quiz.timelimit)
        }
    )

# questions_list = list()
#    for question in quiz.get_guestions():
#        variants = []
#        for variant in question.get_variants(text_only=True):
#            variants.append(variant)
#        shuffle(variants)
#        questions_list.append({question.text: variants})
#    shuffle(questions_list)


def send_answer(request, slug):
    """должен вернуть slug результата"""
    if request.is_ajax():
        test = get_object_or_404(BlueprintTest, slug=slug)
        data = request.POST
        data = dict(data.lists())
        data.pop('csrfmiddlewaretoken')
        max_score = test.get_max_score()
        score = 0
        data = set(
            map(int, list(data.values())[0])
        )
        correct_variants = Variant.objects.filter(
            question__test=test,
            is_correct=True
        ).values_list('pk')
        correct_variants = set([var[0] for var in correct_variants])
        
        score += len(data & correct_variants)
        score -= len(data ^ correct_variants)
        score = 0 if score < 0 else score
        result = Result.objects.create(
            user=request.user,
            test=test,
            result=score,
            max_result=max_score
        )
    return JsonResponse(
        {
            'status': 'success',
            'slug': result.slug,
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
        Result,
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
