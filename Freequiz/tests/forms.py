from django import forms
from django import forms

from .models import (
    Variant,
    BlueprintQuestion,
    Question,
    BlueprintTest,
    Test
)


class BlueprintQuestionForm(forms.ModelForm):
    """Форма для создания вопроса"""
    class Meta:
        model = BlueprintQuestion
        fields = (
            'text',
            'additional',
            'type',
            'time_limit'
        )


class QuestionForm(forms.Form):
    """Форма вопроса"""
    class Meta:
        model = Question
        fields = (
            'text',
            'additional',
            'type',
            'time_limit'
        )
