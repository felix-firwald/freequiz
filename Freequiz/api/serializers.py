from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.response import Response

from quizes.models import (
    Variant,
    Question,
    Quiz,
    Result
)


class VariantSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(
        slug_field='pk',
        queryset=Question.objects.all(),
        write_only=True
    )
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = Variant
        fields = ('pk', 'text', 'is_correct', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)
    pk = serializers.IntegerField(read_only=True)
    quiz = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Quiz.objects.all(),
        write_only=True
    )

    class Meta:
        model = Question
        fields = ('pk', 'text', 'additional', 'type', 'variants', 'quiz')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        lookup_field = 'slug'
        fields = (
            'name',
            'author',
            'slug',
            'description',
            'is_closed',
            'subtract_incorrect',
            'access',
            'attempts',
            'timelimit',
        )


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('slug', 'result', 'max_result', 'user', 'passed')
