from django.contrib import admin
from .models import (
    Variant,
    Question,
    Quiz,
    Result,
)


@admin.action(description='Открыть выбранные тесты')
def make_opened(modeladmin, request, queryset):
    queryset.update(is_closed=False)


@admin.action(description='Закрыть выбранные тесты')
def make_closed(modeladmin, request, queryset):
    queryset.update(is_closed=True)


@admin.action(description='Установить для всех')
def make_for_all(modeladmin, request, queryset):
    queryset.update(access='all')


@admin.action(description='Установить доступ по ссылке')
def make_for_slug(modeladmin, request, queryset):
    queryset.update(access='slug')


@admin.action(description='Снять ограничение на количество попыток')
def set_attempts_null(modeladmin, request, queryset):
    queryset.update(attempts=0)


@admin.action(description='Ограничить одной попыткой')
def set_attempts_one(modeladmin, request, queryset):
    queryset.update(attempts=1)


class VariantInline(admin.StackedInline):
    model = Variant


class QuestionAdmin(admin.ModelAdmin):

    inlines = [VariantInline]
    fields = ('text', 'quiz', 'type')
    list_display = ('text', 'quiz', 'type', 'get_max_score')
    search_fields = ('text', 'quiz', 'type')
    list_filter = ('quiz', 'type')


class QuesInline(admin.StackedInline):
    model = Question


class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'is_closed',
        'subtract_incorrect', 'access', 'timelimit', 'attempts'
    )
    search_fields = ('name', 'author', 'is_closed', 'access')
    list_filter = ('name', 'author', 'is_closed', 'access')
    inlines = [QuesInline]
    actions = [
        make_closed,
        make_opened,
        make_for_all,
        make_for_slug,
        set_attempts_null,
        set_attempts_one
    ]


class ResultAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'passed', 'result', 'max_result', 'slug')
    search_fields = ('quiz', 'user', 'passed', 'result')
    list_filter = ('quiz', 'quiz__author', 'user', 'passed', 'result')
    empty_value_display = 'нельзя редактировать'
    readonly_fields = ('result', 'max_result', 'user', 'quiz')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Result, ResultAdmin)
