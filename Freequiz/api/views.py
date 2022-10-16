from rest_framework import generics

from quizes.models import (
    Variant,
    Question,
    Quiz,
    Result
)
from .serializers import (
    VariantSerializer,
    QuestionSerializer,
    QuizSerializer,
    ResultSerializer
)


class QuizList(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
