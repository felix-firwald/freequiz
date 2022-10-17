from rest_framework import serializers

from quizes import models


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variant
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('text', 'additional', 'type', 'variants')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
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
        model = models.Question
        fields = ('slug', 'result', 'max_result', 'user', 'quiz')
