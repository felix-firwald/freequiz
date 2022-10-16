from random import shuffle

# from django.contrib.sites.models import Site
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import (
    User,
    Variant,
    Question,
    Quiz,
    Result,
)
from notifications.models import Notification

# DOMAIN = Site.objects.get_current().domain


def main_page(request):
    alert = Notification.objects.last()
    tests = Quiz.objects.filter(
        is_closed=False,
        access='all'
    )
    return render(
        request,
        'index.html',
        {
            'quizes': tests,
            'notification': alert
        }
    )


@login_required
def create_quiz(request):
    return redirect(
        'quizes:main'
    )


@login_required
def get_data_for_quiz(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    data = Question.objects.filter(quiz=quiz).values(
        'text', 'type', 'variants__id', 'variants__text')
    questions_dict = dict()
    for question in data:
        questions_dict.setdefault(
            question['text'], []
        ).append(
            [question['variants__id'], question['variants__text'], question['type']]
        )

    return JsonResponse(
        {
            'questions': questions_dict,
            'timelimit': int(quiz.timelimit)
        }
    )


def send_answer(request, slug):
    """должен вернуть slug результата"""
    if request.is_ajax():
        quiz = get_object_or_404(Quiz, slug=slug)
        data = request.POST
        data = dict(data.lists())
        data.pop('csrfmiddlewaretoken')
        try:
            data = set(
                map(int, list(data.values())[0])
            )
        except IndexError:
            return JsonResponse(
                {
                    'status': False,
                    'error': 'Не дано ответа ни на один вопрос'
                }
            )
        correct_variants = Variant.objects.filter(
            question__quiz=quiz,
            is_correct=True
        ).values_list('pk')
        max_score = len(correct_variants)
        correct_variants = set([var[0] for var in correct_variants])
        score = 0
        score += len(data & correct_variants)
        if quiz.subtract_incorrect:
            score -= len(correct_variants - data)
        score = 0 if score < 0 else score
        result = Result.objects.create(
            user=request.user,
            quiz=quiz,
            result=score,
            max_result=max_score
        )
    return JsonResponse(
        {
            'status': True,
            'score': score,
            'max_score': max_score,
            'slug': result.get_absolute_url(),
        }
    )


@login_required
def quiz(request, slug):
    quiz = get_object_or_404(
        Quiz,
        slug=slug
    )
    times = quiz.attempts
    if not times == 0:
        if Result.objects.filter(
            user=request.user,
            quiz=quiz
        ).count() >= times:
            context = {
                'is_passed': True,
                'attempts': times
            }
            return render(
                request,
                'start_test.html',
                context
            )
    context = {
        'slug': quiz.slug,
        'is_closed': quiz.is_closed,
        'is_passed': False,
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
    quiz = get_object_or_404(
        Quiz,
        slug=slug
    )
    if quiz.author == request.user:
        quiz.delete()
        return redirect(
            'quizes:main'
        )
    return redirect(
        'quizes:quiz',
        slug
    )


@login_required
def edit_quiz(request):
    return redirect(
        'quizes:main'
    )


def quiz_result(request, result):
    result = get_object_or_404(
        Result,
        slug=result
    )
    return render(
        request,
        'result.html',
        {'data': result}
    )


@login_required
def my_results(request):
    results = request.user.quizes_results.all()
    return render(
        request,
        'my_results',
        {'data': results}
    )
