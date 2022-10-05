from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.contrib.auth import get_user_model

User = get_user_model()

TYPES_OF_QUESTION = [
    ('radio', 'Один правильный ответ'),
    ('checkbox', 'Несколько правильных ответов'),
    ('textfield', 'Текстовое поле')
]

TYPES_OF_ACCESS = [
    ('all', 'Доступ для всех'),
    ('slug', 'Доступ только по ссылке'),
]


class Variant(models.Model):
    text = models.CharField(max_length=120)
    question = models.ForeignKey(
        'BlueprintQuestion',
        on_delete=models.CASCADE,
        related_name='variants'
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Variant {self.text[:15]}'


class BlueprintQuestion(models.Model):
    text = models.CharField(max_length=160)
    test = models.ForeignKey(
        'BlueprintTest',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    additional = models.TextField(null=True)
    type = models.CharField(
        max_length=50,
        choices=TYPES_OF_QUESTION
    )
    time_limit = models.IntegerField(
        default=120,
        validators=[
            MinValueValidator(10),
            MaxValueValidator(3599)
        ]
    )
    max_score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    def __str__(self):
        return f'Question {self.text[:15]}'


class Question(models.Model):
    blueprint = models.ForeignKey(
        'BlueprintQuestion',
        null=True,
        on_delete=models.SET_NULL,
        related_name='answers'
    )
    test = models.ForeignKey(
        'Test',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    max_score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'blueprint', 'test'],
                name='user can answer only once at one test'
            )
        ]


class BlueprintTest(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=60)
    description = models.TextField(null=True)
    slug = models.SlugField(unique=True)
    access = models.CharField(
        max_length=50,
        choices=TYPES_OF_ACCESS
    )
    is_closed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique name of test by one author'
            )
        ]

    def __str__(self):
        return f'Test {self.slug[:15]}'


class Test(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tests'
    )
    test = models.ForeignKey(
        BlueprintTest,
        on_delete=models.DO_NOTHING,
        related_name='results'
    )
    passed = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    result = models.IntegerField()
    max_result = models.IntegerField()

    class Meta:
        ordering = ['passed']
