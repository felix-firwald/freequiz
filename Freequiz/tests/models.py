from functools import reduce

from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

TYPES_OF_QUESTION = [
    ('radio', 'Один правильный ответ'),
    ('checkbox', 'Несколько правильных ответов'),
]

TYPES_OF_ACCESS = [
    ('all', 'Доступ для всех'),
    ('slug', 'Доступ только по ссылке'),
]


class Variant(models.Model):
    text = models.CharField(max_length=120, verbose_name='текст')
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='variants',
        verbose_name='вопрос'
    )
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'вариант'
        verbose_name_plural = 'варианты'

    def __str__(self):
        return f'Вариант: {self.text[:50]}'


class Question(models.Model):

    text = models.CharField(max_length=160, verbose_name='текст')
    test = models.ForeignKey(
        'Test',
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='тест'
    )
    additional = models.TextField(
        null=True,
        blank=True,
        verbose_name='дополнительная информация'
    )
    type = models.CharField(
        max_length=50,
        choices=TYPES_OF_QUESTION
    )

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def get_max_score(self):
        return self.variants.filter(is_correct=True).count()

    def get_variants(self, text_only=False):
        if text_only:
            return self.variants.values_list('text')
        return self.variants.all()

    def __str__(self):
        return f'Question {self.text[:15]}'


class Test(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    name = models.CharField(max_length=60, verbose_name='название')
    description = models.TextField(
        null=True,
        blank=True,
        default='Информации о тесте нет',
        verbose_name='описание'
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        default=uuid.uuid4,
        verbose_name='ссылка'
    )
    access = models.CharField(
        max_length=50,
        choices=TYPES_OF_ACCESS,
        verbose_name='доступ'
    )
    is_closed = models.BooleanField(
        default=False,
        verbose_name='закрыт для прохождения'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    timelimit = models.IntegerField(
        default=3600,
        validators=[
            MinValueValidator(300),
            MaxValueValidator(10800)
        ],
        verbose_name='ограничение по времени'
    )

    class Meta:
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'
        ordering = ['created']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique name of test by one author'
            )
        ]

    def get_max_score(self):
        questions = self.questions.all()
        return reduce(
            lambda x, y: x + y, [q.get_max_score() for q in questions]
        )

    def get_guestions(self, text_only=False):
        if self.is_closed:
            return []
        if text_only:
            return self.questions.values_list('text')
        return self.questions.all()

    def __str__(self):
        return f'Test {self.name[:20]}'


class Result(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tests_results',
        verbose_name='пользователь'
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.DO_NOTHING,
        related_name='results',
        verbose_name='тест'
    )
    passed = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата прохождения'
    )
    slug = models.SlugField(
        unique=True,
        default=uuid.uuid4,
        verbose_name='ссылка на результат'
    )
    result = models.IntegerField(verbose_name='набранный балл')
    max_result = models.IntegerField(verbose_name='максимальный балл')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('tests:result', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'результат'
        verbose_name_plural = 'результаты'
        ordering = ['passed']
