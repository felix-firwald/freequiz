from rest_framework import serializers

from quizes import models


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variant
        fields = ('text', 'is_correct', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('text', 'additional', 'type', 'quiz')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        fields = (
            'name',
            'description',
            'is_closed',
            'subtract_incorrect',
            'access',
            'attempts',
            'timelimit'
        )


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('result', 'max_result', 'user', 'quiz')
