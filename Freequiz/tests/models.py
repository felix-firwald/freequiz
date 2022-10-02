from django.db import models
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
        'Question',
        on_delete=models.CASCADE,
        related_name='variants'
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'Variant {self.text[:15]}'


class Question(models.Model):
    text = models.CharField(max_length=160)
    test = models.ForeignKey(
        'Test',
        on_delete=models.CASCADE,
        related_name='questions'
    )
    additional = models.TextField(null=True)
    type = models.CharField(
        max_length=50,
        choices=TYPES_OF_QUESTION
    )

    def __str__(self):
        return f'Question {self.text[:15]}'


class Test(models.Model):
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


class Result(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='results'
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.DO_NOTHING,
        related_name='results'
    )
    slug = models.SlugField(unique=True)
    score = models.IntegerField()

