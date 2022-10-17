from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

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


class QuestionsViewSet(viewsets.ViewSet):
    def list(self, request, slug=None):
        queryset = Question.objects.filter(quiz__slug=slug)
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, slug=None):
        question = Question.objects.create(
            text=request.data['text'],
            additional=request.data['additional'],
            type=request.data['type'],
            quiz=get_object_or_404(Quiz, slug=slug)
        )
        return Response({'question': model_to_dict(question)})

    def perform_destroy(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizList(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
